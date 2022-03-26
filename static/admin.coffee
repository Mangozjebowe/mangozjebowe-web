deleteUser = (id) -> 
	resp = await fetch '/manage/users/delete/'+id
	username = document.getElementById('user-'+id)
	username.remove()
	return await resp.json()