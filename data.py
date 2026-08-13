def numinput(prompt):
    while True:
        try: 
            answer = input(prompt).strip()
            answer = int(answer)
        except(ValueError):
            print("정수를 입력해주세요.")

class InputData:
    def __init__(self):
        pass

    #데이터 수집
    def patterninput(self):
        # 패턴인지 필터인지도 
        #3개 한번에 해도? 

        print("패턴과 필터는 n*n 크기의 정사각형 모양을 갖습니다.")
        size = numinput("n의 값을 입력하세요.: ")
        pattern = []
        for i in range(size):
            r = self.rowinput(size)
            pattern.append(r)
        if len(pattern)!= size:
            print("행 열의 크기가 옳지 않습니다. 다시 시도하세요.")
        else:
            print("정상 입력되었습니다.")
            #패턴 프린트
            #세이브
        #열행개수맞나 봄
        #공백 구별
        pass

    def rowinput(self, i, size):
        while True:
            print("공백으로 열을 구분합니다.")
            a = input(f"{i}번째 행을 입력해주세요.: ")
            spliteda = a.split()

            checkint = 0 
            for A in spliteda: 
                try:
                    int(A)
                except ValueError:
                    print("숫자가 아닌 값이 발견 되었습니다.")
                    checkint =1
                    break 
            if checkint == 1:
                continue

            if len(spliteda) != size:
                print(f"{size}개의 열을 입력해야 합니다.")
                continue

            print(f"{i}번째 행이 입력되었습니다.")
            break
        pass


class LoadData:
    def __init__(self):
        pass

    def load(self):
        #json 파일 읽어옴
        pass


class SaveData: 
    def __init__(self):
        pass

    def save(self):
        #저장함..
        #pattern
        #filter
        #expected는 있을 수도 없을수도 사이즈별로정리하는게좋수도 아닐수도 
        pass

class normalizeData:
    def __init__(self):
        pass

    #데이터 전처리
    def norm_label():
        #라벨 정규화 
        pass