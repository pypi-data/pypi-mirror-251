import math
import csv


def estimate_population_size(csv_file, sample_size, observed_unique_count, confidence_level=0.95, margin_of_error=0.05):
    """
    サンプルサイズから母集団の数を推定します。

    :param sample_size: サンプルの行数
    :param observed_unique_count: サンプル中のユニークな要素の数
    :param confidence_level: 信頼度（デフォルトは95%）
    :param margin_of_error: 信頼区間の幅（デフォルトは5%）
    :return: 母集団の推定値と信頼区間
    """
    
    try:
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            sample_size = sum(1 for row in csv_reader)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {csv_file}")
    z_score = 0.5 * (1 + math.erf((1 - confidence_level) / math.sqrt(2)))
    estimated_population = (observed_unique_count ** 2 / sample_size) * (1 / margin_of_error ** 2)
    lower_bound = estimated_population / (1 + (estimated_population - 1) / sample_size * z_score ** 2)
    upper_bound = estimated_population / (1 + (estimated_population - 1) / sample_size * z_score ** 2 / sample_size)

    return estimated_population, (lower_bound, upper_bound)