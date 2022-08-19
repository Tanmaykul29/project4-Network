like = document.querySelectorAll(".liked");

edit = document.querySelectorAll(".edit");
text_area = document.querySelectorAll(".textarea");

like.forEach((element) => {
  like_handeler(element);
});

edit.forEach((element) => {
  element.addEventListener("click", () => {
    edit_handeler(element);
  });
});

text_area.forEach((element) => {
  element.addEventListener("keyup", (e) => {
    if (e.keyCode == 13 && e.shiftKey) return;
    if (e.keyCode === 13) edit_handeler(element);
  });
});

function edit_post(id, post) {
  form = new FormData();
  form.append("id", id);
  form.append("post", post.trim());

  fetch("/edit_post/", {
    method: "POST",
    body: form,
  }).then((res) => {
    document.querySelector(`#post-content-${id}`).textContent = post;
    document.querySelector(`#post-content-${id}`).style.display = "block";
    document.querySelector(`#post-edit-${id}`).style.display = "none";
    document.querySelector(`#post-edit-${id}`).value = post.trim();
  });
}

function edit_handeler(element) {
  id = element.getAttribute("data-id");
  edit_btn = document.querySelector(`#edit-btn-${id}`);
  if (edit_btn.textContent == "Edit") {
    document.querySelector(`#post-content-${id}`).style.display = "none";
    document.querySelector(`#post-edit-${id}`).style.display = "block";
    edit_btn.textContent = "Save";
    edit_btn.setAttribute("class", "text-success edit");
  } else if (edit_btn.textContent == "Save") {
    edit_post(id, document.querySelector(`#post-edit-${id}`).value);

    edit_btn.textContent = "Edit";
    edit_btn.setAttribute("class", "text-primary edit");
  }
}

function like_handeler(element) {
  element.addEventListener("click", () => {
    id = element.getAttribute("data-id");
    is_liked = element.getAttribute("data-is_liked");
    icon = document.querySelector(`#post-like-${id}`);
    count = document.querySelector(`#post-count-${id}`);

    form = new FormData();
    form.append("id", id);
    form.append("is_liked", is_liked);
    fetch("/like/", {
      method: "POST",
      body: form,
    })
      .then((res) => res.json())
      .then((res) => {
        if (res.status == 201) {
          if (res.is_liked === "yes") {
            icon.src = "https://img.icons8.com/plasticine/100/000000/like.png";
            element.setAttribute("data-is_liked", "yes");
          } else {
            icon.src =
              "https://img.icons8.com/carbon-copy/100/000000/like--v2.png";
            element.setAttribute("data-is_liked", "no");
          }
          count.textContent = res.like_count;
        }
      })
      .catch(function (res) {
        alert("Network Error. Please Check your connection.");
      });
  });
}



//post = request.POST.get('post')
//        try:
//            post = Post.objects.get(id=post_id)
//            if post.user == request.user:
//                post.post = new_post.strip()
//                post.save()
//                return JsonResponse({}, status=201)
//        except:
//            return JsonResponse({}, status=404)
//
//    return JsonResponse({}, status=400)
//
////
////@login_required
////@csrf_exempt
////def addpost(request):
////    if request.method == "POST":
////        post = request.POST.get("post")
////        if len(post) != 0:
////            obj = Post()
////            obj.post = post
////            obj.user = request.user
////            obj.save()
////            context = {
////                "status": 201,
////                "post_id": obj.id,
////                "username": request.user.username,
////                "timestamp": obj.timestamp.strftime("%B %d, %Y, %I:%M %p"),
////            }
////            return JsonResponse(context, status=201)
////    return JsonResponse({}, status=400)
