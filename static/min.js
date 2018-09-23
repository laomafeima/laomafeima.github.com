function totop()
{
    if(window.pageYOffset < 1)
    {
        clearInterval(document.interval_id);
    }
    else
    {
        height = window.pageYOffset * 0.975
        window.scroll(0, height)
    }
}

function back_top()
{
    document.interval_id = setInterval("totop();", 4);
    return false;
}

document.onscroll = function()
{
    if(window.pageYOffset > 400)
    {
        var aEle = document.getElementById("back-top");
        if(!aEle)
        {
            aEle = document.createElement("a");
            aEle.id = "back-top";
            aEle.href = "#go-back-home";
            aEle.title = "返回顶部";
            aEle.innerText = "^";
            aEle.onclick = back_top;
            document.body.appendChild(aEle);
        }
    }
    else
    {
        var aEle = document.getElementById("back-top");
        if(aEle)
        {
            document.body.removeChild(document.getElementById("back-top"));
        }
    }
}
