from keywordsHandler import KeywordsHandler

#this is first priority phrases
tier_1_list = ["người lao động", "người sử dụng lao động", "bảo hiểm thất nghiệp", "đào tạo, bồi dưỡng, nâng cao trình độ kỹ năng nghề",
               "trợ cấp thất nghiệp", "tư vấn, giới thiệu việc làm", "quỹ bảo hiểm thất nghiệp", "học nghề"]

#this is second prioriy phrases
tier_2_list = ["quyền", "nghĩa vụ", "covid-19", "đối tượng", "mức", "thủ tục", "nguyên tắc", "chế độ", "tham gia", "đóng", "thời gian", "điều kiện", "hồ sơ", "giải quyết", "thực hiện",
               "hưởng", "nộp", "thời gian", "thời điểm", "tạm dừng", "tiếp tục", "chấm dứt", "chuyển nơi", "đề nghị", "bảo hiểm", "y tế", "thông báo", "tìm kiếm", "việc làm", "hỗ trợ", "tổ chức", "nguồn","bảo lưu"]

#init data to store priored phrases
data = KeywordsHandler([tier_1_list,tier_2_list])
