class Analyze:
    def __init__(self):
        pass

    def mac_calculate(self, pattern, filter_data):
        """N x N 패턴과 필터의 MAC 점수를 계산한다."""

        pattern_size = len(pattern)
        filter_size = len(filter_data)

        if pattern_size != filter_size:
            raise ValueError("패턴과 필터의 크기가 일치하지 않습니다.")

        for row in pattern:
            if len(row) != pattern_size:
                raise ValueError("패턴이 정사각형 배열이 아닙니다.")

        for row in filter_data:
            if len(row) != filter_size:
                raise ValueError("필터가 정사각형 배열이 아닙니다.")

        score = 0.0

        for i in range(pattern_size):
            for j in range(pattern_size):
                score += pattern[i][j] * filter_data[i][j]

        return score