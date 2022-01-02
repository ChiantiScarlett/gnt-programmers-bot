TIER_LIST = ['B5', 'B4', 'B3', 'B2', 'B1', 'S5', 'S4', 'S3', 'S2', 'S1',
             'G5', 'G4', 'G3', 'G2', 'G1', 'P5', 'P4', 'P3', 'P2', 'P1',
             'D5', 'D4', 'D3', 'D2', 'D1', 'R5', 'R4', 'R3', 'R2', 'R1']

TIER_NAME_MAP = {
    'B5': '브론즈5',
    'B4': '브론즈4',
    'B3': '브론즈3',
    'B2': '브론즈2',
    'B1': '브론즈1',
    'S5': '실버5',
    'S4': '실버4',
    'S3': '실버3',
    'S2': '실버2',
    'S1': '실버1',
    'G5': '골드5',
    'G4': '골드4',
    'G3': '골드3',
    'G2': '골드2',
    'G1': '골드1',
    'P5': '플래티넘5',
    'P4': '플래티넘4',
    'P3': '플래티넘3',
    'P2': '플래티넘2',
    'P1': '플래티넘1',
    'D5': '다이아몬드5',
    'D4': '다이아몬드4',
    'D3': '다이아몬드3',
    'D2': '다이아몬드2',
    'D1': '다이아몬드1',
    'R5': '루비5',
    'R4': '루비4',
    'R3': '루비3',
    'R2': '루비2',
    'R1': '루비1',
}

TIER_NORMALIZATION_MAP = {'V': '5', 'IV': '4', 'III': '3', 'II': '2', 'I': '1',
                          '브론즈': 'B', '브': 'B', 'bronze': 'B',
                          '실버': 'S', '실': 'S', 'silver': 'S',
                          '골드': 'G', '골': 'G', 'gold': 'G',
                          '플레티넘': 'P', '플래티넘': 'P', '플레': 'P', '플래': 'P',
                          '플': 'P', 'platinum': 'P',
                          '다이아몬드': 'D', '다이어몬드': 'D', '다이아': 'D', '다이어': 'D',
                          '다': 'D', '다': 'D', 'diamond': 'D',
                          '루비': 'R', '루': 'R', 'ruby': 'R'}
TIER_NORMALIZATION_MAP_KEYS = list(TIER_NORMALIZATION_MAP.keys())
TIER_NORMALIZATION_MAP_KEYS.sort(reverse=True)


WEEKDAY_ENG_TO_INT = {
    'SUNDAY': 0,
    'MONDAY': 1,
    'TUESDAY': 2,
    'WEDNESDAY': 3,
    'THURSDAY': 4,
    'FRIDAY': 5,
    'SATURDAY': 6
}
WEEKDAY_INT_TO_ENG = {v: k for k, v in WEEKDAY_ENG_TO_INT.items()}
WEEKDAY_ENG_TO_KOR = {
    'SUNDAY': '일요일',
    'MONDAY': '월요일',
    'TUESDAY': '화요일',
    'WEDNESDAY': '수요일',
    'THURSDAY': '목요일',
    'FRIDAY': '금요일',
    'SATURDAY': '토요일',
}
