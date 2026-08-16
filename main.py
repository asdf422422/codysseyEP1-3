from data import InputData, LoadData, NormalizeData
from calc import Analyze
from eval import Evaluator
from benchmark import Benchmark


def run_user_mode():
    print("\n===== 사용자 입력 모드 =====")

    input_data = InputData()
    analyzer = Analyze()
    evaluator = Evaluator()
    benchmark = Benchmark(analyzer)

    # --------------------------------
    # 크기 N은 한 번만 입력
    # --------------------------------
    print("\n[입력 크기]")
    size = input_data.sizeinput()

    print(f"\n모든 입력은 {size} x {size} 크기로 입력합니다.")

    # --------------------------------
    # 필터 A 입력
    # --------------------------------
    print("\n[필터 A 입력]")
    filter_a = input_data.matrixinput(
        size,
        "필터 A"
    )

    # --------------------------------
    # 필터 B 입력
    # --------------------------------
    print("\n[필터 B 입력]")
    filter_b = input_data.matrixinput(
        size,
        "필터 B"
    )

    # --------------------------------
    # 패턴 입력
    # --------------------------------
    print("\n[패턴 입력]")
    pattern = input_data.matrixinput(
        size,
        "패턴"
    )

    # --------------------------------
    # MAC 계산
    # --------------------------------
    score_a = analyzer.mac_calculate(
        pattern,
        filter_a
    )

    score_b = analyzer.mac_calculate(
        pattern,
        filter_b
    )

    # --------------------------------
    # 판정
    # --------------------------------
    if score_a > score_b:
        result = "필터 A"

    elif score_b > score_a:
        result = "필터 B"

    else:
        result = "판정 불가 (동점)"

    print("\n===== MAC 결과 =====")
    print(f"필터 A 점수 : {score_a}")
    print(f"필터 B 점수 : {score_b}")
    print(f"판정 결과   : {result}")

    # --------------------------------
    # 성능 측정
    # --------------------------------
    average, operation_count = benchmark.measure(
        pattern,
        filter_a
    )

    print("\n===== 성능 분석 =====")
    print(f"크기             : {size} x {size}")
    print(f"평균 연산 시간   : {average:.6f} ms")
    print(f"연산 횟수        : {operation_count}")


def run_json_mode():
    print("\n===== data.json 분석 모드 =====")

    loader = LoadData("data.json")
    analyzer = Analyze()
    evaluator = Evaluator()
    normalizer = NormalizeData()
    benchmark = Benchmark(analyzer)

    # --------------------------------
    # JSON 로드
    # --------------------------------
    data = loader.load()

    if data is None:
        print("JSON 데이터를 불러오지 못했습니다.")
        return

    # --------------------------------
    # 기본 구조 확인
    # --------------------------------
    if not isinstance(data, dict):
        print("오류: JSON의 최상위 구조가 올바르지 않습니다.")
        return

    if "filters" not in data:
        print("오류: filters가 없습니다.")
        return

    if "patterns" not in data:
        print("오류: patterns가 없습니다.")
        return

    filters = data["filters"]
    patterns = data["patterns"]

    if not isinstance(filters, dict):
        print("오류: filters는 객체여야 합니다.")
        return

    if not isinstance(patterns, dict):
        print("오류: patterns는 객체여야 합니다.")
        return

    # --------------------------------
    # 결과 저장
    # --------------------------------
    total = 0
    passed = 0
    failed = 0

    fail_cases = []

    # --------------------------------
    # 각 패턴 처리
    # --------------------------------
    for case_id, case_data in patterns.items():

        total += 1

        print("\n" + "-" * 40)
        print(f"케이스: {case_id}")

        try:
            # ----------------------------
            # case 데이터 확인
            # ----------------------------
            if not isinstance(case_data, dict):
                raise ValueError(
                    "케이스 데이터가 객체가 아닙니다."
                )

            if "input" not in case_data:
                raise ValueError(
                    "input이 없습니다."
                )

            if "expected" not in case_data:
                raise ValueError(
                    "expected가 없습니다."
                )

            pattern = case_data["input"]
            expected_raw = case_data["expected"]

            # ----------------------------
            # case_id에서 크기 추출
            # ----------------------------
            parts = case_id.split("_")

            if len(parts) < 2:
                raise ValueError(
                    "케이스 ID에서 크기를 찾을 수 없습니다."
                )

            size = int(parts[1])

            # ----------------------------
            # expected 정규화
            # ----------------------------
            expected = normalizer.norm_label(
                expected_raw
            )

            if expected is None:
                raise ValueError(
                    f"알 수 없는 expected 라벨: "
                    f"{expected_raw}"
                )

            # ----------------------------
            # 패턴 크기 확인
            # ----------------------------
            if len(pattern) != size:
                raise ValueError(
                    f"패턴 행 개수가 {size}가 아닙니다."
                )

            for row in pattern:
                if len(row) != size:
                    raise ValueError(
                        f"패턴이 {size}x{size}가 아닙니다."
                    )

            # ----------------------------
            # 해당 크기의 필터 찾기
            # ----------------------------
            filter_key = f"size_{size}"

            if filter_key not in filters:
                raise ValueError(
                    f"{filter_key} 필터가 없습니다."
                )

            size_filters = filters[filter_key]

            # ----------------------------
            # Cross / X 필터 찾기
            # ----------------------------
            cross_filter = None
            x_filter = None

            for key, filter_data in size_filters.items():

                label = normalizer.norm_label(key)

                if label == "Cross":
                    cross_filter = filter_data

                elif label == "X":
                    x_filter = filter_data

            if cross_filter is None:
                raise ValueError(
                    "Cross 필터가 없습니다."
                )

            if x_filter is None:
                raise ValueError(
                    "X 필터가 없습니다."
                )

            # ----------------------------
            # 필터 크기 확인
            # ----------------------------
            if len(cross_filter) != size:
                raise ValueError(
                    "Cross 필터의 크기가 올바르지 않습니다."
                )

            if len(x_filter) != size:
                raise ValueError(
                    "X 필터의 크기가 올바르지 않습니다."
                )

            for row in cross_filter:
                if len(row) != size:
                    raise ValueError(
                        "Cross 필터가 정사각형이 아닙니다."
                    )

            for row in x_filter:
                if len(row) != size:
                    raise ValueError(
                        "X 필터가 정사각형이 아닙니다."
                    )

            # ----------------------------
            # MAC 계산
            # ----------------------------
            cross_score = analyzer.mac_calculate(
                pattern,
                cross_filter
            )

            x_score = analyzer.mac_calculate(
                pattern,
                x_filter
            )

            # ----------------------------
            # 판정
            # ----------------------------
            result = evaluator.judge(
                cross_score,
                x_score
            )

            # ----------------------------
            # expected와 비교
            # ----------------------------
            status = evaluator.compare_expected(
                result,
                expected
            )

            print(f"Cross 점수 : {cross_score}")
            print(f"X 점수     : {x_score}")
            print(f"판정       : {result}")
            print(f"Expected   : {expected}")
            print(f"결과       : {status}")

            if status == "PASS":
                passed += 1

            else:
                failed += 1

                fail_cases.append(
                    (case_id, "판정 결과와 expected가 다릅니다.")
                )

        except (ValueError, TypeError, KeyError) as error:

            failed += 1

            reason = str(error)

            print("결과       : FAIL")
            print(f"실패 원인  : {reason}")

            fail_cases.append(
                (case_id, reason)
            )

    # ====================================
    # 성능 분석
    # ====================================

    print("\n" + "=" * 50)
    print("성능 분석")
    print("=" * 50)

    print(
        f"{'크기':<12}"
        f"{'평균 시간(ms)':<20}"
        f"{'연산 횟수(N²)':<20}"
    )

    print("-" * 52)

    # JSON에는 5, 13, 25가 있으므로 측정
    for size in [5, 13, 25]:

        filter_key = f"size_{size}"

        if filter_key not in filters:
            print(
                f"{size}x{size:<8}"
                f"측정 불가 - 필터 없음"
            )
            continue

        size_filters = filters[filter_key]

        cross_filter = None

        for key, filter_data in size_filters.items():

            label = normalizer.norm_label(key)

            if label == "Cross":
                cross_filter = filter_data
                break

        if cross_filter is None:
            print(
                f"{size}x{size:<8}"
                f"측정 불가 - Cross 필터 없음"
            )
            continue

        # 성능 측정을 위한 N x N 패턴
        pattern = []

        for _ in range(size):
            pattern.append([0.0] * size)

        average, operation_count = benchmark.measure(
            pattern,
            cross_filter
        )

        print(
            f"{size}x{size:<8}"
            f"{average:<20.6f}"
            f"{operation_count:<20}"
        )

    # ====================================
    # 결과 리포트
    # ====================================

    print("\n" + "=" * 50)
    print("결과 리포트")
    print("=" * 50)

    print(f"전체 테스트 수 : {total}")
    print(f"통과 수        : {passed}")
    print(f"실패 수        : {failed}")

    if failed > 0:

        print("\n[실패 케이스]")

        for case_id, reason in fail_cases:
            print(f"- {case_id}")
            print(f"  사유: {reason}")

    else:
        print("\n모든 테스트가 PASS입니다.")


def main():

    print("=" * 50)
    print("Mini NPU Simulator")
    print("=" * 50)

    while True:

        print("\n실행 모드를 선택하세요.")
        print("1. 사용자 입력")
        print("2. data.json 분석")
        print("0. 종료")

        choice = input("선택: ").strip()

        if choice == "1":
            run_user_mode()

        elif choice == "2":
            run_json_mode()

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("1, 2, 0 중 하나를 입력해주세요.")


if __name__ == "__main__":
    main()