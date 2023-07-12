// document.addEventListener("DOMContentLoaded", () => {
//   get_imgs();
// });

document.getElementById("send").addEventListener("click", () => {
  upload_say("async");
});

document.getElementById("sync_send").addEventListener("click", () => {
  upload_say("sync");
});

document.getElementById("clear").addEventListener("click", () => {
  document.getElementById("result_messages").innerHTML = "";
});

document.getElementById("call").addEventListener("click", () => {
  call_server();
});

let box = document.getElementById("box")

// get file size when selected
document.getElementById("image_up").addEventListener("change", () => {
  let files = document.getElementById("image_up").files;
  let file_size = files[0].size;
  let mb = file_size / 1024 / 1024;
  document.getElementById("file_size").innerHTML = mb.toFixed(2) + "MB";
});

upload_say = async (type) => {
  let result_messages = document.getElementById("result_messages");
  let says = document.getElementById("says").value;
  let files = document.getElementById("image_up").files;
  let file_name = files[0].name;
  let data = new FormData();
  data.append("name", file_name);
  data.append("image", files[0]);
  data.append("says", says);
  result_messages.innerHTML += "上傳中...\n";
  if (type == "sync") {
    data.append("type", "sync");
  }else{
    data.append("type", "async");
  }

  const options = { method: "POST", body: data };
  const response = await fetch("/upload", options);
  const result = await response.json();
  if (result.ok && type == "async") {
    words = "非同步上傳成功\n"
    result_messages.innerHTML += "非同步上傳成功\n<br>";
    // window.location.href="/"
  } else if (result.ok && type == "sync") {
    result_messages.innerHTML += "同步上傳成功\n<br>";
    // window.location.href="/"
  }
  else {
    console.log("OOPS");
    result_messages.innerHTML += "發生錯誤\n<br>";
  }
};


//顯示全部圖片
get_imgs = async() => {
  const options = { method: "GET" };
  const response = await fetch("/imgs", options);
  const result = await response.json();

  console.log(result)
  for(a of result.data){
  let says = a.says
  let img = "http://dwuiiqlrlr6g5.cloudfront.net/"+a.img_id;

  console.log(says,img)
  let a_box = document.createElement("div")

  //對話
  let say = document.createElement("p")
  let word = document.createTextNode(says)
  say.appendChild(word)
  //圖片
  let pic = document.createElement("img")
  pic.setAttribute("class","pic")
  pic.setAttribute("src",img)

  a_box.appendChild(say)
  a_box.appendChild(pic)
  box.appendChild(a_box)
  }
}

call_server = async () => {
  let result_messages = document.getElementById("result_call");
  result_messages.innerHTML += "呼叫中...\n";
  const options = { method: "GET" };
  const response = await fetch("/call", options);
  const result = await response.json();
  if (result.ok) {
    result_messages.innerHTML += "我在\n";
  } else {
    console.log("OOPS");
    result_messages.innerHTML += "發生錯誤\n";
  }
}