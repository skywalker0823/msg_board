document.addEventListener("DOMContentLoaded", () => {
  get_imgs();
});

document.getElementById("send").addEventListener("click", () => {
  upload_say();
});

let box = document.getElementById("box")

upload_say = async () => {
  let says = document.getElementById("says").value;
  let files = document.getElementById("image_up").files;
  let file_name = files[0].name;
  let data = new FormData();
  data.append("name", file_name);
  data.append("image", files[0]);
  data.append("says", says);

  const options = { method: "POST", body: data };
  const response = await fetch("/upload", options);
  const result = await response.json();
  if (result.ok) {
    console.log("perfect!");
    window.location.href="/"
  } else {
    console.log("OOPS");
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