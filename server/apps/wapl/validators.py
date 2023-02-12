from django.core.exceptions import ValidationError 
from datetime import datetime as d

# 일정 시간 검증 함수
# endTime이 startTime보다 더 이전이면 에러 메세지 리턴
# 시간을 선택하지 않았을 시 시간 설정 요구 에러 메세지 리턴
def validate_plan_time(startTime, endTime):
  msg = '종료 시간이 시작 시간보다 이전일 수 없습니다.'
  
  temp_startTime = startTime.replace('T', " ")
  temp_endTime = endTime.replace('T', " ")
  
  try:
    if d.strptime(temp_startTime, '%Y-%m-%d %H:%M') > d.strptime(temp_endTime, '%Y-%m-%d %H:%M') :
      return msg
    else:
      return ""
  except ValueError:
    msg = '시간을 설정해야 합니다.'
    return msg

# 일정 제목 검증 함수
# 일정 제목의 문자열 길이가 0이면 에러 메세지 리턴
def validate_plan_title(title):
  msg = '일정 제목을 입력해야 합니다.'
  if len(title) == 0:
    return msg
  else:
    return ""
  
# 일정 생성, 수정 검증 함수
# 인자로 검증이 필요한 필드를 넘겨받아 검증 실행
# 하나라도 에러가 있을 시 False와 해당 에러 메세지들 반환
def validate_plan(**kwargs):
  err_msg=[]
  err_msg.append(validate_plan_time(kwargs.get('startTime'), kwargs.get('endTime')))
  err_msg.append(validate_plan_title(kwargs.get("title")))
  return_msg = ''
  for msg in err_msg:
    if len(msg) != 0:
      return_msg += "Error: " + msg + "\n"
  if len(return_msg) == 0:
    return True, return_msg
  else:
    return False, return_msg
  
def validate_comment(comments):
  msg = '댓글을 작성하세요.'
  if len(comments) == 0:
    return False, msg
  else:
    return True, ""

