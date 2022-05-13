from underthesea import word_tokenize, chunk, pos_tag, ner, classify


def filter_words(input_list):
    """
    Input: list of word with pos_tag
    Output: list of string that doesn't contain redundant words in term of tag
    """
    reduced = []
    index = 0
    #print(input_list)
    while index < len(input_list):
        if index+1 < len(input_list):
            if input_list[index][0] == 'tạm' and input_list[index+1][0] == 'dừng':
                reduced.append(('tạm dừng', 'V'))
                index = index + 2
                continue
            elif input_list[index][0] == 'không' and input_list[index+1][1] == 'V':
                reduced.append(input_list[index])
                reduced.append(input_list[index+1])
                index = index + 2
                continue
            elif input_list[index][0] == 'nâng' and input_list[index+1][0] == 'cao':
                reduced.append(('nâng cao', 'V'))
                index = index + 2
                continue
            elif (input_list[index][0] == 'kĩ năng' or input_list[index][0] == 'kỹ năng') and input_list[index+1][0] == 'nghề':
                reduced.append(('kỹ năng nghề', 'N'))
                index = index + 2
                continue
            elif input_list[index][0] == 'học' and input_list[index+1][0] == 'nghề':
                reduced.append(('học nghề', 'N'))
                index = index + 2
                continue

        if input_list[index][1] == 'N' or input_list[index][1] == 'Nc' or input_list[index][1] == 'V':
            reduced.append(input_list[index])
        elif input_list[index][0] == 'bảo hiểm' or input_list[index][0] == 'nghĩa vụ' or input_list[index][0] == 'covid-19' or input_list[index][0] == 'bảo lưu' or input_list[index][0] == 'bưu điện':
            reduced.append((input_list[index][0], 'N'))
        index = index + 1

    if reduced and reduced[-1][1] == 'V':
        data = reduced[-1][0]
        reduced.pop()
        reduced.append((data, 'N'))
    return reduced


def check_unnecessaries(word, word_previous, word_behind):
    """
    Input: current word, previous and behind it\n
    Output: number of words that is considered unnecessary, started from current
    """
    if((word == 'có' and word_behind == 'được')
       or (word == 'diễn' and word_behind == 'ra')
       or ((word == 'các' or word == 'những') and word_behind == 'bước') or (word == 'không' and (word_behind == '?' or word_behind == ''))):
        return 2
    elif(word == 'như thế nào' or word == 'về' or word == 'phải'
         or word == 'cần' or word == 'tính' or word == 'được'
         or word == 'theo' or (word == 'có' and word_previous != 'không') or word == 'gồm'
         or word == 'trường hợp' or word == 'bị' or word == 'khi'
         or word == 'là' or word == 'như thế nào'
         or word == 'bao nhiêu' or word == 'bao gồm' or word == 'hiện nay'):
        return 1
    else:
        return 0

def convert_synonyms(word, word_previous, word_behind):
    """
    Input: current word, previous and behind it\n
    Output: return synonym that is determined to use instead of input word
    """

    if (word == 'xin' or word == 'yêu cầu') and word_behind != 'đề nghị':
        return "đề nghị"
    elif word == 'nhận' and (word_behind == 'trợ cấp' or word_behind == 'hỗ trợ'):
        return "hưởng"
    elif word == 'thay đổi' and word_behind == 'nơi':
        return "chuyển"
    elif word == 'mong muốn' and word_previous == 'có':
        return "nhu cầu"
    elif word == 'dừng' and word_previous != 'tạm':
        return "chấm dứt"
    elif word == 'trao' and word_behind == 'quyền':
        return "ủy"
    else:
        return dictSynonyms(word)


def dictSynonyms(word):
    return {
        'thời hạn': "thời gian",
        'xử lí':  "giải quyết",
        'xử lý':  "giải quyết",
        'duyệt':  "giải quyết",
        'giấy tờ':  "hồ sơ",
        'văn bản':  "hồ sơ",
        'corona':  "covid-19",
        'ncov':  "covid-19",
        'gửi':  "nộp",
        'gửi':  "nộp",
        'trình tự': "thủ tục",
        "quy trình": "thủ tục",
        "trách nhiệm": "nghĩa vụ",
        "kết thúc": "chấm dứt",
        "đối với": "khi",
        "ngưng": "tạm dừng",
        "ngừng": "tạm dừng"
    }.get(word, word)