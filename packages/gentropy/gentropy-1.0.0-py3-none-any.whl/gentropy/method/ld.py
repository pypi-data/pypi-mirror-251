"""Performing linkage disequilibrium (LD) operations."""
from __future__ import annotations

from typing import TYPE_CHECKING

from pyspark.sql import functions as f

from gentropy.dataset.study_locus import StudyLocus

if TYPE_CHECKING:
    from pyspark.sql import Column

    from gentropy.dataset.ld_index import LDIndex
    from gentropy.dataset.study_index import StudyIndex


class LDAnnotator:
    """Class to annotate linkage disequilibrium (LD) operations from GnomAD."""

    @staticmethod
    def _calculate_weighted_r_overall(ld_set: Column) -> Column:
        """Aggregation of weighted R information using ancestry proportions.

        Args:
            ld_set (Column): LD set

        Returns:
            Column: LD set with added 'r2Overall' field
        """
        return f.transform(
            ld_set,
            lambda x: f.struct(
                x["tagVariantId"].alias("tagVariantId"),
                # r2Overall is the accumulated sum of each r2 relative to the population size
                f.aggregate(
                    x["rValues"],
                    f.lit(0.0),
                    lambda acc, y: acc
                    + f.coalesce(
                        f.pow(y["r"], 2) * y["relativeSampleSize"], f.lit(0.0)
                    ),  # we use coalesce to avoid problems when r/relativeSampleSize is null
                ).alias("r2Overall"),
            ),
        )

    @staticmethod
    def _add_population_size(ld_set: Column, study_populations: Column) -> Column:
        """Add population size to each rValues entry in the ldSet.

        Args:
            ld_set (Column): LD set
            study_populations (Column): Study populations

        Returns:
            Column: LD set with added 'relativeSampleSize' field
        """
        # Create a population to relativeSampleSize map from the struct
        populations_map = f.map_from_arrays(
            study_populations["ldPopulation"],
            study_populations["relativeSampleSize"],
        )
        return f.transform(
            ld_set,
            lambda x: f.struct(
                x["tagVariantId"].alias("tagVariantId"),
                f.transform(
                    x["rValues"],
                    lambda y: f.struct(
                        y["population"].alias("population"),
                        y["r"].alias("r"),
                        populations_map[y["population"]].alias("relativeSampleSize"),
                    ),
                ).alias("rValues"),
            ),
        )

    @classmethod
    def ld_annotate(
        cls: type[LDAnnotator],
        associations: StudyLocus,
        studies: StudyIndex,
        ld_index: LDIndex,
    ) -> StudyLocus:
        """Annotate linkage disequilibrium (LD) information to a set of studyLocus.

        This function:
            1. Annotates study locus with population structure information from the study index
            2. Joins the LD index to the StudyLocus
            3. Adds the population size of the study to each rValues entry in the ldSet
            4. Calculates the overall R weighted by the ancestry proportions in every given study.

        Args:
            associations (StudyLocus): Dataset to be LD annotated
            studies (StudyIndex): Dataset with study information
            ld_index (LDIndex): Dataset with LD information for every variant present in LD matrix

        Returns:
            StudyLocus: including additional column with LD information.
        """
        return (
            StudyLocus(
                _df=(
                    associations.df
                    # Drop ldSet column if already available
                    .select(*[col for col in associations.df.columns if col != "ldSet"])
                    # Annotate study locus with population structure from study index
                    .join(
                        studies.df.select("studyId", "ldPopulationStructure"),
                        on="studyId",
                        how="left",
                    )
                    # Bring LD information from LD Index
                    .join(
                        ld_index.df,
                        on=["variantId", "chromosome"],
                        how="left",
                    )
                    # Add population size to each rValues entry in the ldSet if population structure available:
                    .withColumn(
                        "ldSet",
                        f.when(
                            f.col("ldPopulationStructure").isNotNull(),
                            cls._add_population_size(
                                f.col("ldSet"), f.col("ldPopulationStructure")
                            ),
                        ),
                    )
                    # Aggregate weighted R information using ancestry proportions
                    .withColumn(
                        "ldSet",
                        f.when(
                            f.col("ldPopulationStructure").isNotNull(),
                            cls._calculate_weighted_r_overall(f.col("ldSet")),
                        ),
                    )
                    .drop("ldPopulationStructure")
                ),
                _schema=StudyLocus.get_schema(),
            )
            ._qc_no_population()
            ._qc_unresolved_ld()
        )
