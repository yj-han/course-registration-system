from enum import Enum, unique

@unique
class MajorType(str, Enum):
    MAJOR = "Major"
    MINOR = "Minor"
    DOUBLE_MAJOR = "Double Major"
    ELSE = "Else"


@unique
class Major(str, Enum):
    URP = "URP"
    HSS = "인문사회과학부"
    CC = "공통필수"
    IP = "지식재산 부전공 프로그램"
    PD = "미래자동차 학제전공"
    GT = "조천식녹색교통대학원"
    PH = "물리학과"
    BS = "생명과학과"
    CH = "화학과"
    MAS = "수리과학과"
    ICE = "정보통신공학과"
    ITP = "글로벌IT기술대학원프로그램"
    IE = "산업및시스템공학과"
    ID = "산업디자인학과"
    NQE = "원자력및양자공학과"
    MS = "신소재공학과"
    EE = "전기및전자공학부"
    CS = "전산학부"
    CE = "건설및환경공학과"
    CBE = "생명화학공학과"
    BiS = "바이오및뇌공학과"
    MSB = "기술경영학부"
    GCT = "문화기술대학원"
    MSE = "의과학대학원"
    RE = "로봇공학학제전공"
    CTP = "문화기술학 부전공 프로그램"
    STP = "과학기술정책대학원 | 과학기술정책학 부전공 프로그램"
    KSE = "지식서비스공학대학원"
    NST = "나노과학기술대학원"
    SEP = "소프트웨어대학원프로그램"
    ITM = "기술경영전문대학원"
    SPE = "우주탐사공학학제전공"
    IS = "정보보호대학원"
    MIP = "지식재산대학원프로그램"
    SJ = "과학저널리즘대학원프로그램"
    ECN = "경제학 부전공 프로그램"
    FS = "미래전략대학원프로그램"
    CD = "Capstone Design"
    GFS = "문술미래전략대학원"
    BCE = "뇌인지공학프로그램"
    CoE = "공과대학"
    ME = "기계공학과"
    AE = "항공우주공학과"
    KEI = "K-School"
    TS = "융합인재학부"
    AI = "AI대학원"
    BME = "경영공학부"
    BIT = "테크노경영대학원"
    BAF = "금융전문대학원"
    BIM = "정보미디어경영대학원"
    BGM = "녹색성장대학원"
    FRESH = "새내기과정학부"
    ELSE = "기타"
    
    @classmethod
    def value_of(cls, value):
        for enum in cls.__members__.values():
            if value in enum.value:
                return enum
        else:
            return cls.ELSE

    