var image = document.getElementById("Like")
                var baseURL = "{% static 'network/FullHeart.png' %}"
                console.log(baseURL)

                $(document).ready( function() {
                    function editPost(val, id) {

                        fetch('/editPost', {
                        method: 'PUT',
                        body: JSON.stringify({
                            user: {{user.id}},
                            postId: id,
                            post: val
                        })
                        })
                        .then(response => response.json())
                        .then(result => {
                            // Print result
                            console.log(result);
                    });    
                    
                }

                    $('[id^="edit"]').click(function() {
                        //alert("clicked")
                        // alert($(this).attr('id'));
                        
                        var edit = $(this).attr('id');
                        var id = edit.substring(4);
                        var text = "text" + id;
                        var save = "save" + id;
                        var editedText = "editedText" + id;
                        console.log(text)
                        $('#'+text).editable();
                        $('#'+text).focus();
                        $('#'+edit).hide();
                        $('#'+save).show();

                    });

                    $('[id^="save"]').click(function() {
                        //alert("clicked")
                        // alert($(this).attr('id'));
                        
                        var save = $(this).attr('id');
                        var id = save.substring(4);
                        var text = "text" + id;
                        var edit = "edit" + id;
                        var editedText = "editedText" + id;
                        console.log(text)
                        var post = $('#'+text).text();
                        console.log(post)
                        editPost(post,id);
                        $('#'+save).hide();
                        $('#'+edit).show();

                    });
                });


                function updateLike(id, update) {

                    fetch('/updateLike', {
                    method: 'PUT',
                    body: JSON.stringify({
                        user: {{user.id}},
                        postId: id,
                        counter: update
                    })
                    })
                    .then(response => response.json())
                    .then(result => {
                        // Print result
                        console.log(result);
                    });
                } 

                function getLikes(postId) {
                    console.log("start..");
                    fetch('/getLikes/' + postId)
                    .then(response => response.json())
                    .then(likes => {
                        console.log(likes);
                        var id = "numlikes" + postId
                        console.log(likes.likes);
                        $('#'+id).html(likes.likes);
                    });
                    console.log("function");

                }


                $('[id^="like"]').click(function() {
                    var like = $(this).attr('id');
                    var id = like.substring(4);
                    var image = "image" + id;
                    var curScr = $('#'+image).prop('src');
                    var update = 0;
                    // console.log(like)
                    // console.log(image)
                    console.log(curScr)
                    if (curScr == "http://127.0.0.1:8000/static/network/emptyHeart.png") {
                        $('#'+image).attr('src', 'http://127.0.0.1:8000/static/network/FullHeart.png');
                        update = 1;
                        console.log(update);
                        updateLike(id, update);
                        setTimeout(getLikes, 100, id);
                        // getLikes(id);
                        return false;
                        
                    }
                    else{
                        $('#'+image).attr('src', 'http://127.0.0.1:8000/static/network/emptyHeart.png');
                        updateLike(id, update);
                        console.log(update);
                        setTimeout(getLikes, 100, id);
                        //getLikes(id);
                        return false;
                    }
                    return false;
                });