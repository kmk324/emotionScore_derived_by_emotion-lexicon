from konlpy.tag import Komoran
import csv


# Function for update sentence_emotion_state
def sumState(indexJ):
    sentence_state['NEG'] = sentence_state['NEG'] + float(morphemes_info[indexJ]['NEG'])
    sentence_state['NEUT'] = sentence_state['NEUT'] + float(morphemes_info[indexJ]['NEUT'])
    sentence_state['POS'] = sentence_state['POS'] + float(morphemes_info[indexJ]['POS'])


sentence_state = dict()
sentence_state['NEG'] = 0.0 # it is negative score from sentence.
sentence_state['NEUT'] = 0.0 # it is neutral score from sentence.
sentence_state['POS'] = 0.0 # it is positive score from sentence.

komoran = Komoran()
# Open a csv file
reader = csv.DictReader(open('./lexicon/polarity.csv', "rt", encoding='utf-8'))

morphemes_info = []  # list for saving read csv file
for i, line in enumerate(reader):
    morphemes_info.append(line)
    morphemes_info[i]['ngram'] = morphemes_info[i]['ngram'].split(';')
    for j in range(len(morphemes_info[i]['ngram'])):
        morphemes_info[i]['ngram'][j] = morphemes_info[i]['ngram'][j].split('/')

user_input = input("감정분석할 문장을 입력해주세요\n")
input_nouns = komoran.pos(user_input) # komoran 모듈을 사용하여 형태소 추출.

matchCount = 0  # 매칭되는 케이스의 수를 카운팅하는 변수.
forComp = []  # 연속적으로 매칭 되는 케이스 판별을 위한 임시 리스트.
i = 0  # 루프문에 사용되는 인덱스 초기화

# Kosac 감성어 사전과 input_sentence의 형태소를 활용 하여 문장의 부정 중립 긍정 정도를 계산한다.
while i < len(input_nouns):
    forComp.clear()
    forComp.append(list(input_nouns[i]))
    matchCount = 0
    for j in range(len(morphemes_info)):
        if (forComp == morphemes_info[j]['ngram']):  # i=i+1
            matchCount += 1
            lastMatchJ = j
            if (i + matchCount < len(input_nouns)):  # input_nouns의 i 다음 인덱스가 있을 시.
                forComp.append(list(input_nouns[i + matchCount]))
            else:  # input_nouns의 i 다음 인덱스가 없을 시.
                sumState(j)
                i = i + matchCount
                break
        else:
            if (j == len(morphemes_info) - 1):  # j가 마지막까지 돌았는데 일치하는 항목이 없는 경우.
                if (matchCount >= 1):  # 적어도 한 번 매칭 된 적이 있다.
                    sumState(lastMatchJ)
                    i = i + matchCount
                else:  # 한 번도 매칭 된 적이 없다.
                    i = i + 1

# print the sentence_state
# Ex) input <- 늦은 밤 골목길은 무섭고 두렵다.   output -> 'Neg':5.0085, 'Neut':0.64752, 'Pos': 1.678865091
print(sentence_state)


