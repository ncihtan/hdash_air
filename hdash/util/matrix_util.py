"""Matrix Utility."""
import pandas as pd
from natsort import natsorted
from hdash.db.matrix import Matrix
from hdash.stats.completeness_summary import CompletenessSummary
from hdash.util.categories import Categories


class MatrixUtil:
    """Matrix Utility Class."""

    CLINICAL_TIER_1_2 = "clinical_tier1_2"
    CLINICAL_TIER_3 = "clinical_tier3"
    SINGLE_CELL = "single_cell"
    BULK = "bulk"
    IMAGE_OTHER = "image_other"
    OTHER = "other"

    def __init__(self, atlas_id, completeness_summary: CompletenessSummary):
        """Create Matrix Utility."""
        self.atlas_id = atlas_id
        self.completeness_summary = completeness_summary
        self.matrix_list = []
        self.categories = Categories()
        self.current_order = 0

        # Matrix 1
        self._build_clinical_matrix(
            MatrixUtil.CLINICAL_TIER_1_2,
            self.categories.clinical_tier1_2_list,
            "Clinical Data Matrix: Tiers 1 and 2",
        )

        # Matrix 2
        self._build_clinical_matrix(
            MatrixUtil.CLINICAL_TIER_3,
            self.categories.clinical_tier3_list,
            "Clinical Data Matrix: Tier 3",
        )

        # Matrix 3
        self.single_cell_assay_list = []
        self.single_cell_assay_list.extend(self.categories.sc_rna_list)
        self.single_cell_assay_list.extend(self.categories.sc_atac_list)
        self._build_assay_matrix(
            MatrixUtil.SINGLE_CELL,
            self.single_cell_assay_list,
            "Assay Matrix: Single Cell Data",
        )

        # Matrix 4
        self.bulk_assay_list = []
        self.bulk_assay_list.extend(self.categories.bulk_rna_list)
        self.bulk_assay_list.extend(self.categories.bulk_wes_list)
        self.bulk_assay_list.extend(self.categories.bulk_methylation_seq)
        self.bulk_assay_list.extend(self.categories.hi_c_seq_list)
        self._build_assay_matrix(
            MatrixUtil.BULK, self.bulk_assay_list, "Assay Matrix: Bulk Data"
        )

        # Matrix 5
        self.image_assay_list = []
        self.image_assay_list.extend(self.categories.image_list)
        self._build_assay_matrix(
            MatrixUtil.IMAGE_OTHER,
            self.image_assay_list,
            "Assay Matrix: Core Imaging",
        )

        # Matrix 6
        self.other_assay_list = []
        self.other_assay_list.extend(self.categories.visium_list)
        self.other_assay_list.extend(self.categories.slide_seq_list)
        self.other_assay_list.extend(self.categories.electron_microscopy_list)
        self.other_assay_list.extend(self.categories.mass_spec_list)
        self.other_assay_list.extend(self.categories.rppa_list)
        self.other_assay_list.extend(self.categories.other_assay_list)
        self._build_assay_matrix(
            MatrixUtil.OTHER, self.other_assay_list, "Assay Matrix: Other"
        )

    def _build_clinical_matrix(self, heatmap_type, category_list, label):
        """Build Clinical Data Heatmap."""
        headers = ["ParticipantID"]
        data = []
        for category in category_list:
            if "Tier3" in category:
                shorter = category[:8] + ".."
                headers.append(shorter)
            else:
                headers.append(category)
        for participant_id in self.completeness_summary.graph_flat.participant_id_set:
            current_row = [participant_id]
            for category in category_list:
                value = 0
                if self.completeness_summary.has_data(participant_id, category):
                    value = 1
                current_row.append(value)
            data.append(current_row)
        self._create_matrix(heatmap_type, data, headers, label)

    def _build_assay_matrix(self, heatmap_type, category_list, label):
        """Build Assay Data Heatmap."""
        headers = ["BiospecimenID"]
        data = []
        for category in category_list:
            headers.append(category)
        b_ids = self.completeness_summary.graph_flat.biospecimen_id_set
        b_ids = natsorted(b_ids)
        for biospecimen_id in b_ids:
            total_sum = 0
            current_row = [biospecimen_id]
            for category in category_list:
                value = 0
                if self.completeness_summary.has_data(biospecimen_id, category):
                    value = 1
                current_row.append(value)
                total_sum += value
            if total_sum > -0:
                data.append(current_row)
        self._create_matrix(heatmap_type, data, headers, label)

    def _create_matrix(self, matrix_type, data, headers, label):
        """Create Heatmap Object."""
        data_frame = pd.DataFrame(data, columns=headers)
        matrix_id = self.atlas_id + "_" + matrix_type
        matrix = Matrix()
        matrix.matrix_id = matrix_id
        matrix.atlas_id = self.atlas_id
        matrix.order = self.current_order
        matrix.label = label
        matrix.content = data_frame.to_csv(index=False)
        self.matrix_list.append(matrix)
        self.current_order += 1
