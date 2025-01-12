import pandas as pd
import requests
import datetime

# CSV 파일 읽기 (탭 문자를 구분자로 사용)
df = pd.read_csv('station.csv', delimiter='\t', encoding='utf-8')

# 시간 문자열을 분 단위로 변환하는 함수
def convert_to_minutes(time_str):
    minutes, seconds = map(int, time_str.split(':'))
    return minutes + seconds / 60

# 출발역에서 환승역까지의 소요시간을 계산하는 함수
def calculate_start_to_transfer(df, start_row, transfer_row1):
    start_index = start_row.index[0]
    transfer_index = transfer_row1.index[0]
    start_to_transfer = df.loc[min(start_index, transfer_index):max(start_index, transfer_index), '시간(분)'].sum()
    return start_to_transfer

# 환승역에서 도착역까지의 소요시간을 계산하는 함수
def calculate_transfer_to_end(df, transfer_row2, end_row):
    transfer_index = transfer_row2.index[0]
    end_index = end_row.index[0]
    transfer_to_end = df.loc[min(transfer_index, end_index):max(transfer_index, end_index), '시간(분)'].sum()
    return transfer_to_end

# CSV 파일로부터 각 호선의 역 목록을 읽어옴
def read_station_csv(filename):
    df = pd.read_csv(filename, sep=',', encoding='utf-8')
    line_stations = {}
    for line, stations_str in zip(df['호선'], df['역명']):
        stations = eval(stations_str)
        line_stations[line] = stations
    return line_stations

# 호선의 역 목록
line_stations = read_station_csv('stations.csv')

# 방향 구하기 함수
def get_train_direction(station_list, start_station, end_station):
    start_index = station_list.index(start_station)
    end_index = station_list.index(end_station)
    return '하행' if start_index < end_index else '상행'

# 소요 시간을 계산하는 함수
def calculate_time(df, start, transfer, end):
    df['시간(분)'] = df['시간(분)'].apply(convert_to_minutes)

    # 출발역과 환승역, 환승역과 도착역이 동일한 호선인지 확인
    def find_common_line(station1, station2):
        for line1 in df[df['역명'] == station1]['호선'].unique():
            for line2 in df[df['역명'] == station2]['호선'].unique():
                if line1 == line2:
                    return line1
        raise ValueError(f"{station1}와 {station2}가 동일한 호선에 존재하지 않습니다.")

    start_line = find_common_line(start, transfer)
    end_line = find_common_line(transfer, end)

    # 출발역과 환승역의 데이터 행 가져오기
    start_row = df[(df['역명'] == start) & (df['호선'] == start_line)]
    transfer_row1 = df[(df['역명'] == transfer) & (df['호선'] == start_line)]
    transfer_row2 = df[(df['역명'] == transfer) & (df['호선'] == end_line)]
    end_row = df[(df['역명'] == end) & (df['호선'] == end_line)]

    # 출발역에서 환승역까지의 소요시간 계산
    start_to_transfer_time = calculate_start_to_transfer(df, start_row, transfer_row1)

    # 환승역에서 도착역까지의 소요시간 계산
    transfer_to_end_time = calculate_transfer_to_end(df, transfer_row2, end_row)

    total_time = start_to_transfer_time + transfer_to_end_time

    # 호선명을 지하철 호선 ID로 변환
    line_ids = {
        '1': '1001',
        '2': '1002',
        '3': '1003',
        '4': '1004',
        '5': '1005',
        '6': '1006',
        '7': '1007',
        '8': '1008',
        '9': '1009'
    }

    start_line_id = line_ids.get(str(start_line), None)
    end_line_id = line_ids.get(str(end_line), None)

    # 각 구간의 방향 구하기
    if start_line in line_stations and end_line in line_stations:
        start_to_transfer_direction = get_train_direction(line_stations[start_line], start, transfer)
        transfer_to_end_direction = get_train_direction(line_stations[end_line], transfer, end)
    else:
        raise ValueError("호선 데이터가 누락되었습니다.")

    return start_to_transfer_time, transfer_to_end_time, total_time, start_line_id, end_line_id, start_to_transfer_direction, transfer_to_end_direction

# 서울공공데이터 API 키
api_key = '655972707868776f3931486b4e7057'

def get_real_time_train_info(station_name):
    url = f'http://swopenapi.seoul.go.kr/api/subway/{api_key}/json/realtimeStationArrival/0/5/{station_name}'
    response = requests.get(url)
    train_info = response.json()
    
    if 'realtimeArrivalList' not in train_info:
        print("API 응답 오류:", train_info)
        return None
    
    return train_info['realtimeArrivalList']

def print_train_info_at_time(station_name, expected_time, line_id, direction, num_trains=10):
    print(f"\n{station_name}에서의 예상 도착 시간 {expected_time.strftime('%H:%M')} 이후의 열차 정보:")
    train_info = get_real_time_train_info(station_name)
    if train_info is not None:
        trains_with_diff = []
        for train in train_info:
            try:
                arrival_time = int(train['barvlDt']) // 60  # 도착 시간(초 단위)을 분 단위로 변환
                expected_arrival = datetime.datetime.now() + datetime.timedelta(minutes=arrival_time)
                time_diff = abs((expected_arrival - expected_time).total_seconds())
                if expected_arrival >= expected_time and train['subwayId'] == line_id and direction == train['updnLine']:   # 예상 도착 시간 이후의 정보 중 해당 방면 열차만 선택
                    trains_with_diff.append((train, time_diff))
                    
            except (KeyError, ValueError, TypeError):
                continue

        # time_diff를 기준으로 정렬하여 가장 근접한 num_trains개의 열차 정보를 선택
        trains_with_diff.sort(key=lambda x: x[1])
        closest_trains = trains_with_diff[:num_trains]
        
        if closest_trains:
            for train, diff in closest_trains:
                arrival_time = int(train['barvlDt']) // 60
                expected_arrival = (datetime.datetime.now() + datetime.timedelta(minutes=arrival_time)).strftime('%H:%M')
                print(f" - {train['trainLineNm']}: {train['arvlMsg2']} (예상 도착 시간: {expected_arrival})")
        else:
            print(f" - {station_name}에서의 열차 정보가 없습니다.")
    else:
        print("실시간 열차 정보를 가져오지 못했습니다.")

# 메인 함수
def main():
    start_station = input("출발역을 입력하세요: ")
    transfer_station = input("환승역을 입력하세요: ")
    end_station = input("도착역을 입력하세요: ")
    
    try:
        start_to_transfer, transfer_to_end, total_time, start_line_id, end_line_id, start_to_transfer_direction, transfer_to_end_direction = calculate_time(df, start_station, transfer_station, end_station)
        print(f"출발역에서 환승역까지의 소요시간: {start_to_transfer:.0f}분")
        print(f"환승역에서 도착역까지의 소요시간: {transfer_to_end:.0f}분")
        print(f"총 소요시간은 {total_time:.0f}분입니다.")
        
        # 현재 시간 계산
        now = datetime.datetime.now()
        transfer_time = now + datetime.timedelta(minutes=start_to_transfer)
        end_time = now + datetime.timedelta(minutes=total_time)

        print(f"\n환승역 {transfer_station}의 예상 도착 시간: {transfer_time.strftime('%H:%M')}")
        print(f"도착역 {end_station}의 예상 도착 시간: {end_time.strftime('%H:%M')}")

        # 예상 도착 시간에 맞추어 출발역과 환승역의 열차 정보 출력
        print_train_info_at_time(start_station, now, start_line_id, start_to_transfer_direction)
        # 예상 도착 시간에 맞추어 환승역과 도착역의 열차 정보 출력
        print_train_info_at_time(transfer_station, transfer_time, end_line_id, transfer_to_end_direction)

        # 출발역의 실제 열차 도착시간을 구함
        train_info = get_real_time_train_info(start_station)
        if train_info is not None:
            closest_train = None
            min_diff = float('inf')
            for train in train_info:
                if train['subwayId'] == start_line_id and train['updnLine'] == start_to_transfer_direction:
                    arrival_time = int(train['barvlDt']) // 60
                    expected_arrival = datetime.datetime.now() + datetime.timedelta(minutes=arrival_time)
                    diff = abs((expected_arrival - now).total_seconds())
                    if diff < min_diff:
                        min_diff = diff
                        closest_train = train
            
            if closest_train:
                arrival_time = int(closest_train['barvlDt']) // 60
                closest_train_time = now + datetime.timedelta(minutes=arrival_time)
                transfer_time = closest_train_time + datetime.timedelta(minutes=start_to_transfer)
            else:
                print(f"{start_station}에서 출발할 열차 정보를 찾을 수 없습니다.")
        else:
            print("실시간 열차 정보를 가져오지 못했습니다.")
            
               
        # 환승역의 실제 열차 도착시간을 구함
        transfer_train_info = get_real_time_train_info(transfer_station)
        if transfer_train_info is not None:
            closest_transfer_train = None
            min_transfer_diff = float('inf')
            for train in transfer_train_info:
                if train['subwayId'] == end_line_id and train['updnLine'] == transfer_to_end_direction:
                    transfer_arrival_time = int(train['barvlDt']) // 60
                    expected_transfer_arrival = datetime.datetime.now() + datetime.timedelta(minutes=transfer_arrival_time)
                    transfer_diff = abs((expected_transfer_arrival - transfer_time).total_seconds())
                    if transfer_diff < min_transfer_diff:
                        min_transfer_diff = transfer_diff
                        closest_transfer_train = train

            if closest_transfer_train:
                transfer_arrival_time = int(closest_transfer_train['barvlDt']) // 60
                closest_transfer_train_time = datetime.datetime.now() + datetime.timedelta(minutes=transfer_arrival_time)
                end_time = closest_transfer_train_time + datetime.timedelta(minutes=transfer_to_end)
                        
                print(f"\n출발역 {start_station}의 실제 열차 도착 시간: {closest_train_time.strftime('%H:%M')}")
                print(f"환승역 {transfer_station}의 실제 열차 도착 시간: {closest_transfer_train_time.strftime('%H:%M')}")
                print(f"도착역 {end_station}의 예상 도착 시간: {end_time.strftime('%H:%M')}")

                # 예상 도착 시간에 맞추어 환승역의 열차 정보 출력
                print_train_info_at_time(transfer_station, closest_transfer_train_time, end_line_id, transfer_to_end_direction)
            else:
                print(f"{transfer_station}에서 출발할 열차 정보를 찾을 수 없습니다.")
        else:
            print("실시간 열차 정보를 가져오지 못했습니다.")
            
    
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
