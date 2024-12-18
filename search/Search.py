# 검색화면 프롬프트 (구현 : 김종권)
# 미완

from MovieDTO import MovieData
from movie.MovieInfo import display_movie_details
from movie.MovieInfo import load_user_data

def display_search_page(user_id):

    print("\n" + "=" * 40)
    print("[영화 검색]")
    print("('0'을 입력할 시 이전 화면으로 돌아갑니다.)")
    print("\n" + "=" * 40)

    while True:

        user_input = input("찾고자 하는 영화 제목을 입력하세요(또는 '#<감독 아이디>'를 입력하여 해당 감독이 감독한 영화 목록을 확인하세요.): ").strip()

        if user_input == "0":
            break
        else:
            if len(user_input) == 0 or len(user_input) > 50:
                print("잘못된 입력입니다. 최소 한 글자 이상, 최대 50자 이하로 입력해주세요.")
                continue

            searched_list = search_movies(user_input)
            if len(searched_list) == 0:
                print("검색 결과가 없습니다!")
                continue

            print("\n" + "=" * 40)
            print("[검색 결과]")
            current_page = 1

            while True:

                fravorite_list = load_user_data(user_id)["favorited_movies"]

                # 총 페이지 수 계산
                pages = (len(fravorite_list) - 1) // 10 + 1
                print("=" * 40)
                print(f"({current_page}페이지)")

                # 현재 페이지의 시작 인덱스와 끝 인덱스 계산
                start_index = (current_page - 1) * 10
                end_index = min(start_index + 10, len(searched_list))

                rated_movies = load_user_data(user_id)["rated_movies"]
                # 영화 제목을 출력
                for i in range(start_index, end_index):
                    movie_id = searched_list[i]
                    rated_indicator = "✅" if movie_id in rated_movies else "☑️"
                    title = MovieData.movies[movie_id]["title"]
                    directors = MovieData.movies[movie_id]["directors"]
                    average_rating = MovieData.movies[movie_id]["average_rating"]
                    rating_count = MovieData.movies[movie_id]["rating_count"]
                    print(f"[{i - start_index + 1}] {title} (감독명: {directors} / 평점: {average_rating} / 평가 인원 수: {rating_count}) {rated_indicator}")

                print("=" * 40)
                print("이전 페이지: - / 다음 페이지: + / 뒤로가기: 0")

                while True:
                    user_input = input("상세정보를 조회할 영화 번호를 입력하세요: ").strip()
                    
                    # 사용자 입력에 따른 페이지 전환 또는 영화 상세 정보 조회
                    if user_input == "-":
                        if current_page == 1:
                            print("\n첫 페이지입니다.")
                            print("=" * 40)
                        else:
                            current_page -= 1
                            break
                    elif user_input == "+":
                        if current_page == pages:
                            print("\n마지막 페이지입니다.")
                            print("=" * 40)
                        else:
                            current_page += 1
                            break
                    elif user_input == "0":
                        print("=" * 40)
                        return
                    else:
                        try:
                            # 사용자가 입력한 번호가 1부터 (현재 페이지의 영화 수)까지인지 확인
                            selected_index = int(user_input) - 1  # 1부터 시작하므로 -1
                            if 0 <= selected_index < (end_index - start_index):
                                movie_id = searched_list[start_index + selected_index]  # 실제 ID 찾기
                                display_movie_details(user_id, movie_id)
                                break
                            else:
                                print("유효하지 않은 영화 번호입니다.")
                        except ValueError:
                            print("유효한 입력을 해주세요.")  # 입력이 숫자가 아닐 경우 처리

def search_movies(keyword):
    matched_movie_ids = []  # 검색된 movie_id를 저장할 리스트

    # keyword의 공백 제거 및 소문자 처리
    processed_keyword = keyword.replace(" ", "").lower()

    # '#'으로 시작하는 검색인 경우 (감독 아이디를 통한 검색)
    if keyword.startswith("#"):  # 입력이 "#"으로 시작하면
        try:
            director_id = int(keyword[1:])  # "#" 다음 숫자를 추출 시도
            for movie_id, movie_data in MovieData.movies.items():
                if director_id in movie_data["director_ids"]:  # director_ids에 해당 ID가 있는지 확인
                    matched_movie_ids.append(movie_id)  # 조건을 만족하면 추가
        except ValueError:  # 숫자로 변환되지 않으면
            print("# 뒤는 숫자여야 합니다.")  # 예외 메시지 출력
    # 일반 검색 (영화 제목 및 감독명 기반)
    else:
        for movie_id, movie_data in MovieData.movies.items():
            # title과 director의 공백 제거 및 소문자 처리
            processed_title = movie_data["title"].replace(" ", "").lower()
            processed_directors = movie_data["directors"].replace(" ", "").lower()

            # title이나 director 중 하나라도 keyword를 포함하면 추가
            if processed_keyword in processed_title or processed_keyword in processed_directors:
                matched_movie_ids.append(movie_id)

    return matched_movie_ids
