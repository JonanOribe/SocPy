function commentReplyToogle(parent_id){
    let parent_path = "post_detail_parent_"+parent_id;
    const row = document.getElementById(parent_path);
    row.classList.contains('d-none')? row.classList.remove('d-none'):row.classList.add('d-none');
}