/*
일정 생성 클릭 시 실행 함수
input 태그를 배열로 가져와(inputs) 순서대로 변수에 저장
순서: startTime, endTime, location, title, content (이후 데이터 추가 시 순서 주의)
저장 후 Js에서 일정 화면에 추가 해야할 듯 함
method: POST
*/
const plan_create = async () => {
  const url = "/create";
  inputs = document.getElementsByTagName("input");
  const data = {
    startTime: inputs[0].value + " " + inputs[1].value,
    endTime: inputs[0].value + " " + inputs[2].value,
    location: inputs[3].value,
    title: inputs[4].value,
    content: inputs[5].value,
  };

  const { newPlan } = await axios.post(url, data);
};

/*
  일정 삭제 클릭 시 실행 함수
  선택한 일정의 id 값을 인자로 넘김
  method: POST
  */
const plan_delete = async (id) => {
  const url = "/delete";
  await axios.post(url, {
    id,
  });
};
/*
    일정 수정 버튼 클릭 시 실행 함수
    일정 생성과 로직은 동일하며 추가로 일정 객체의 id 값을 추가로 넘김
    순서: startTime, endTime, location, title, content (이후 데이터 추가 시 순서 주의)
    method: POST
    */
const plan_update = async (id) => {
  const url = "/update";
  inputs = document.getElementsByTagName("input");
  const data = {
    id,
    startTime: inputs[0].value + " " + inputs[1].value,
    endTime: inputs[0].value + " " + inputs[2].value,
    location: inputs[3].value,
    title: inputs[4].value,
    content: inputs[5].value,
  };

  const { newPlan } = await axios.post(url, data);
};
