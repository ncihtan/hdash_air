"""ID Utility Class."""
from hdash.util.categories import Categories


class IdUtil:
    """ID Utility Class."""

    HTAN_PARTICIPANT_ID = "HTAN Participant ID"
    HTAN_BIOSPECIMEN_ID = "HTAN Biospecimen ID"
    HTAN_PARENT_ID = "HTAN Parent ID"
    HTAN_PARENT_FILE_ID = "HTAN Parent Data File ID"
    HTAN_DATA_FILE_ID = "HTAN Data File ID"
    HTAN_PARENT_BIOSPECIMEN_ID = "HTAN Parent Biospecimen ID"
    ADJACENT_BIOSPECIMEN_ID = "Adjacent Biospecimen IDs"
    ACCESSORY_SYNAPSE_ID = "Accessory Synapse ID"

    def __init__(self):
        """Init ID Maps."""
        self.categories = Categories()
        self.primary_id_map = {
            Categories.BIOSPECIMEN: IdUtil.HTAN_BIOSPECIMEN_ID,
            Categories.SRRS_BIOSPECIMEN: IdUtil.HTAN_BIOSPECIMEN_ID,
            Categories.ACCESSORY_MANIFEST: IdUtil.ACCESSORY_SYNAPSE_ID,
        }

        #  All Clinical Categories have the Same Primary ID
        for clinical_category in self.categories.all_clinical:
            self.primary_id_map[clinical_category] = IdUtil.HTAN_PARTICIPANT_ID

        self.parent_id_map = {
            Categories.BIOSPECIMEN: IdUtil.HTAN_PARENT_ID,
            Categories.SRRS_BIOSPECIMEN: IdUtil.HTAN_PARENT_ID,
            Categories.SC_RNA_SEQ_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.BULK_RNA_SEQ_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.BULK_WES_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.IMAGING_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.IMAGING_LEVEL_2: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.SRRS_IMAGING_LEVEL2: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.SC_ATAC_SEQ_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.OTHER_ASSAY: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.VISIUM_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.VISIUM_LEVEL_2: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.VISIUM_AUX_LEVEL_2: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.SLIDE_SEQ_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.BULK_METHYLATION_SEQ_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.EX_SEQ_MINIMAL: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.ACCESSORY_MANIFEST: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.HI_C_SEQ_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.MASS_SPEC_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
            Categories.ELECTRON_MICROSCOPY_LEVEL_1: IdUtil.HTAN_PARENT_BIOSPECIMEN_ID,
        }

    def get_primary_id_column(self, category):
        """Get Primary ID Column for the specified category of data."""
        return self.primary_id_map.get(category, IdUtil.HTAN_DATA_FILE_ID)

    def get_parent_id_column(self, category):
        """Get Parent ID Column for the specified category of data."""
        if category in self.categories.all_clinical:
            return None
        return self.parent_id_map.get(category, IdUtil.HTAN_PARENT_FILE_ID)

    def get_adjacent_id_column(self, category):
        """Get Adjacent ID Column, if available."""
        if category == Categories.BIOSPECIMEN:
            return IdUtil.ADJACENT_BIOSPECIMEN_ID
        return None
