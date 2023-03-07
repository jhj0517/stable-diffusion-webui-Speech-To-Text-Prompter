function updateTxt2ImgPrompt(text) {
    if (text.trim() === '') {
        return
    }
    var textarea = gradioApp().querySelector('#txt2img_prompt textarea')
    textarea.value = text
    updateInput(textarea)
    textarea.scrollIntoView()
}

function updateTxt2ImgNegPrompt(text) {
    if (text.trim() === '') {
        return
    }
    var textarea = gradioApp().querySelector('#txt2img_neg_prompt textarea')
    textarea.value = text
    updateInput(textarea)
    textarea.scrollIntoView()
}

function updateImg2ImgPrompt(text) {
    if (text.trim() === '') {
        return
    }
    var textarea = gradioApp().querySelector('#img2img_prompt textarea')
    textarea.value = text
    updateInput(textarea)
    textarea.scrollIntoView()
}

function updateImg2ImgNegPrompt(text) {
    if (text.trim() === '') {
        return
    }
    var textarea = gradioApp().querySelector('#img2img_neg_prompt textarea')
    textarea.value = text
    updateInput(textarea)
    textarea.scrollIntoView()
}
