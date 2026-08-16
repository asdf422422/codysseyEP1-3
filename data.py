import json


def numinput(prompt):
    """숫자를 입력받아 float으로 반환한다."""
    while True:
        value = input(prompt)

        try:
            return float(value)
        except ValueError:
            print("숫자를 입력해주세요.")


class InputData:
    """콘솔에서 패턴/필터 데이터를 입력받는 클래스"""

    def __init__(self):
        pass

    def sizeinput(self):
        """양의 정수 크기 N을 입력받는다."""
        while True:
            value = input("n의 값을 입력하세요.: ")

            try:
                size = int(value)

                if size <= 0:
                    print("크기는 1 이상의 정수여야 합니다.")
                    continue

                return size

            except ValueError:
                print("크기는 정수로 입력해주세요.")

    def rowinput(self, row_number, size):
        """한 행을 입력받아 float 리스트로 반환한다."""

        while True:
            value = input(
                f"{row_number}번째 행을 입력해주세요.: "
            )

            split_value = value.split()

            if len(split_value) != size:
                print(
                    f"입력 형식 오류: "
                    f"각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요."
                )
                continue

            row = []

            try:
                for value in split_value:
                    row.append(float(value))

            except ValueError:
                print("입력 형식 오류: 숫자가 아닌 값이 발견되었습니다.")
                continue

            print(f"{row_number}번째 행이 입력되었습니다.")
            return row

    def matrixinput(self, size, name="데이터"):
        """지정된 크기의 N x N 행렬을 입력받는다."""

        print(f"{name}을(를) {size} x {size} 크기로 입력합니다.")

        matrix = []

        for row_number in range(1, size + 1):
            row = self.rowinput(row_number, size)
            matrix.append(row)

        print(f"{name} 입력이 완료되었습니다.")

        return matrix

    def patterninput(self):
        """N x N 크기의 패턴을 입력받는다."""

        print("패턴과 필터는 n*n 크기의 정사각형 모양을 갖습니다.")

        size = self.sizeinput()

        return self.matrixinput(size, "패턴")

class LoadData:
    """JSON 데이터를 읽어오는 클래스"""

    def __init__(self, filename="data.json"):
        self.filename = filename

    def load(self):
        """data.json을 읽어서 Python 객체로 반환한다."""

        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {self.filename}")
            return None

        except json.JSONDecodeError:
            print(f"JSON 형식이 올바르지 않습니다: {self.filename}")
            return None


class SaveData:
    """데이터를 JSON으로 저장하는 클래스"""

    def __init__(self, filename="data.json"):
        self.filename = filename

    def save(self, data):
        """Python 데이터를 JSON 파일로 저장한다."""

        try:
            with open(self.filename, "w", encoding="utf-8") as file:
                json.dump(
                    data,
                    file,
                    ensure_ascii=False,
                    indent=4
                )

            print(f"데이터가 저장되었습니다: {self.filename}")
            return True

        except OSError as error:
            print(f"파일 저장 중 오류가 발생했습니다: {error}")
            return False


class NormalizeData:
    """데이터의 라벨을 프로그램 내부 표준 라벨로 변환한다."""

    LABEL_MAP = {
        "+": "Cross",
        "cross": "Cross",
        "x": "X"
    }

    def __init__(self):
        pass

    def norm_label(self, label):
        """
        입력 라벨을 표준 라벨로 변환한다.

        + / cross -> Cross
        x -> X
        """

        if not isinstance(label, str):
            return None

        label = label.strip().lower()

        return self.LABEL_MAP.get(label)

    def normalize_filter_key(self, key):
        """
        filter의 키에서 Cross/X 라벨을 표준화한다.

        예:
        cross -> Cross
        x -> X
        """

        if not isinstance(key, str):
            return None

        # size_5_cross 같은 키가 들어오는 경우를 대비
        parts = key.lower().split("_")

        if "cross" in parts:
            return "Cross"

        if "x" in parts:
            return "X"

        return None