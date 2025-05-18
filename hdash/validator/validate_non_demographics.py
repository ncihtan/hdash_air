"""Validation Rule."""

from hdash.util.categories import Categories
from hdash.validator.validation_rule import ValidationRule
from hdash.util.id_util import IdUtil
from hdash.synapse.meta_map import MetaMap


class ValidateNonDemographics(ValidationRule):
    """Verify IDs in Non-Demographics Clinical Data Files."""

    def __init__(self, meta_map: MetaMap):
        """Construct new Validation Rule."""
        super().__init__(
            "H_NON_DEM",
            "Non-Demographic clinical data use same IDs as demographics file.",
        )
        categories = Categories()
        demographics_list = meta_map.get_meta_file_list(Categories.DEMOGRAPHICS)
        if len(demographics_list) == 0:
            self.add_error_message("Cannot assess.  No Demographics File.")
        else:
            demog_id_list = []
            for demographics_file in demographics_list:
                data_frame = demographics_file.data_frame
                if data_frame is not None:
                    demog_id_list.extend(
                        data_frame[IdUtil.HTAN_PARTICIPANT_ID].to_list()
                    )
            for category in categories.all_clinical:
                self.__check_file(category, meta_map, demog_id_list)

    def __check_file(self, category, meta_map: MetaMap, demog_id_list):
        if meta_map.has_category(category):
            clinical_file_list = meta_map.get_meta_file_list(category)
            for clinical_file in clinical_file_list:
                data_frame = clinical_file.data_frame
                if data_frame is not None:
                    participant_id_list = data_frame[
                        IdUtil.HTAN_PARTICIPANT_ID
                    ].to_list()
                    for participant_id in participant_id_list:
                        if participant_id not in demog_id_list:
                            msg = (
                                f"Clinical file:  {category} "
                                f"contains ID:  {participant_id}"
                                ", but this ID is not in Demographics File"
                            )
                            self.add_error(msg, clinical_file)
