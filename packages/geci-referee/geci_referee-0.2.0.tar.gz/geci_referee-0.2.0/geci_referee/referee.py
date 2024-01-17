def calculate_true_positive(all_data):
    cat_detected = all_data["cat_detected"]
    with_cat = all_data["with_cat"]
    return cat_detected & with_cat


def calculate_true_negative(all_data):
    return all_data["cat_not_detected"] & all_data["without_cat"]


def calculate_false_positive(all_data):
    return all_data["cat_detected"] - all_data["with_cat"]


def calculate_false_negative(all_data):
    return all_data["cat_not_detected"] - all_data["without_cat"]


def calculate_accuracy(all_data):
    all_classifications = _calculate_all_classifications(all_data)
    correct_classifications = _calculate_correct_classifications(all_data)
    return correct_classifications / all_classifications


def calculate_sensibility(all_data):
    binary_classification = _classify(all_data)
    number_of_true_positives = len(binary_classification["true_positive"])
    number_of_with_cat = len(all_data["with_cat"])
    return number_of_true_positives / number_of_with_cat


def calculate_specificity(all_data):
    binary_classification = _classify(all_data)
    number_of_true_negatives = len(binary_classification["true_negative"])
    number_of_without_cat = len(all_data["without_cat"])
    return number_of_true_negatives / number_of_without_cat


def calculate_average_true_rate(all_data):
    specificity = calculate_specificity(all_data)
    sensibility = calculate_sensibility(all_data)
    return (specificity + sensibility) / 2


def _calculate_all_classifications(all_data):
    binary_classification = _classify(all_data)
    return len(
        binary_classification["true_positive"]
        | binary_classification["true_negative"]
        | binary_classification["false_positive"]
        | binary_classification["false_negative"]
    )


def _calculate_correct_classifications(all_data):
    binary_classification = _classify(all_data)
    return len(binary_classification["true_positive"] | binary_classification["true_negative"])


def _classify(all_data):
    true_positive = calculate_true_positive(all_data)
    true_negative = calculate_true_negative(all_data)
    false_positive = calculate_false_positive(all_data)
    false_negative = calculate_false_negative(all_data)
    return {
        "true_positive": true_positive,
        "true_negative": true_negative,
        "false_positive": false_positive,
        "false_negative": false_negative,
    }
