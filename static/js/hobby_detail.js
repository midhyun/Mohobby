const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
console.log(dayjs('2022-01-01'))
dayjs.extend(dayjs_plugin_relativeTime)
const commentInput = document.querySelector('#commentinput')

const submitComment = function (e) {
    event.preventDefault();
    const commentForm = document.querySelector(`#${e}`)
    const pk = event.target.dataset.hobbyId;

    axios({
        method: 'post',
        url: `/hobby/${pk}/comment_create`,
        headers: { 'X-CSRFToken': csrftoken},
        data: new FormData(commentForm)
    })
    .then(response => {
        const commentList = document.querySelector('#comment-list')
        commentList.textContent = ""
        for (let i=0; i < response.data.comments_data.length; i++){
            commentList.insertAdjacentHTML('beforeend', `<hr>
            <div class="comment-elem" >
                <img class="comment-image" src="https://dummyimage.com/80x80/000/fff" alt="">
              <div>
                <p>${ response.data.comments_data[i].user }</p>
                <p>${ response.data.comments_data[i].content }</p>
                <div>
                  <p class="text-muted" style="font-size:12px"><span>${dayjs(response.data.comments_data[i].created_at).fromNow()}</span> <span>좋아요 0개</span> <span>답글달기</span> <ion-icon name="ellipsis-horizontal"></ion-icon></p>
                </div>
              </div>
            </div>`)};
        commentInput.value = ""

    })

}