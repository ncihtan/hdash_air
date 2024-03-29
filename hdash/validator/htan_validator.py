"""Core HTAN Validator."""

from typing import List
from hdash.db.validation import Validation, ValidationError
from hdash.graph.htan_graph import HtanGraph
from hdash.validator.validation_rule import ValidationRule
from hdash.validator.validate_demographics import ValidateDemographics
from hdash.validator.validate_biospecimens import ValidateBiospecimens
from hdash.validator.validate_primary_ids import ValidatePrimaryIds
from hdash.validator.validate_entity_ids import ValidateEntityIds
from hdash.validator.validate_non_demographics import ValidateNonDemographics
from hdash.validator.validate_links import ValidateLinks
from hdash.validator.validate_categories import ValidateCategories
from hdash.synapse.meta_map import MetaMap


class HtanValidator:
    """Core HTAN Validator."""

    def __init__(self, atlas_id, meta_map: MetaMap, htan_graph: HtanGraph):
        """Construct a new HTAN Validator for one atlas."""
        self.counter = 0
        self.atlas_id = atlas_id
        self.meta_map = meta_map
        self.graph = htan_graph
        self.validation_results: List[Validation] = []
        self.__validate()

    def get_validation_results(self) -> List[Validation]:
        """Get the list of validation results."""
        return self.validation_results

    def __validate(self):
        # Categories Validation
        check0 = ValidateCategories(self.meta_map)
        self._add_results(check0)

        # Clinical Validation
        check1 = ValidateDemographics(self.atlas_id, self.meta_map)
        self._add_results(check1)

        if check1.validation_passed():
            check2 = ValidateNonDemographics(self.meta_map)
            self._add_results(check2)

        # Biospecimen Validation
        check3 = ValidateBiospecimens(self.meta_map)
        self._add_results(check3)

        # ID Checks
        check4 = ValidatePrimaryIds(self.atlas_id, self.meta_map)
        self._add_results(check4)

        # Link Integrity
        check5 = ValidateLinks(self.graph)
        self._add_results(check5)

        # Synapse IDs
        check6 = ValidateEntityIds(self.meta_map)
        self._add_results(check6)

    def _add_results(self, validation_rule: ValidationRule):
        """Add Validation Results."""
        validation_results = Validation(
            self.atlas_id,
            validation_rule.validation_code,
            validation_rule.validation_text,
        )
        validation_results.validation_order = self.counter
        self.counter += 1
        error_list: List[ValidationError] = []
        error_counter = 0
        for error_msg in validation_rule.error_list:
            error = ValidationError()
            error.error_msg = error_msg
            error.order = error_counter
            error_counter += 1
            error_list.append(error)
        validation_results.error_list = error_list
        self.validation_results.append(validation_results)
