follow_btn = document.querySelector("#follow-btn");
follow_btn.addEventListener("click", (e) => {
  user = follow_btn.getAttribute("data-user");
  action = follow_btn.textContent.trim();
  form = new FormData();
  form.append("user", user);
  form.append("action", action);
  fetch("/follow/", {
    method: "POST",
    body: form,
  })
    .then((res) => res.json())
    .then((res) => {
      if (res.status == 201) {
        follow_btn.textContent = res.action;
        document.querySelector(
          "#follower"
        ).textContent = `Followers ${res.follower_count}`;
      }
    });
});



//        if action == "Follow":
//            try:
//                # add user to current user's following list
//                user = User.objects.get(username=user)
//                profile = Profile.objects.get(user=request.user)
//                profile.following.add(user)
//                profile.save()
//
//                # add current user to  user's follower list
//                profile = Profile.objects.get(user=user)
//                profile.follower.add(request.user)
//                profile.save()
//                return JsonResponse({
//                    "status": 301,
//                    "action": "Unfollow",
//                    "follower_count": profile.follower.count()}, status=201)
//            except:
//                return JsonResponse({}, status=404)
//        else:
//            try:
//
//                user = User.objects.get(username=user)
//                profile = Profile.objects.get(user=request.user)
//                profile.following.remove(user)
//                profile.save()
//
//
//                profile = Profile.objects.get(user=user)
//                profile.follower.remove(request.user)
//                profile.save()
//                return JsonResponse({'status': 201, 'action': "Follow", "follower_count": profile.follower.count()}, status=201)
//            except:
//                return JsonResponse({}, stat