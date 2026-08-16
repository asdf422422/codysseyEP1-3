class Evaluator:
    """
    MAC 점수를 비교하여 Cross / X / UNDECIDED를 판정한다.
    """

    def __init__(self, epsilon=1e-9):
        self.epsilon = epsilon

    def judge(self, cross_score, x_score):
        """
        Cross와 X의 MAC 점수를 비교한다.

        차이가 epsilon보다 작으면 동점으로 판단한다.
        """

        if abs(cross_score - x_score) < self.epsilon:
            return "UNDECIDED"

        if cross_score > x_score:
            return "Cross"

        return "X"

    def compare_expected(self, result, expected):
        """
        실제 판정 결과와 expected를 비교한다.

        result와 expected는 표준 라벨이어야 한다.
        """

        if result == expected:
            return "PASS"

        return "FAIL"