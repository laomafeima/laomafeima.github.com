function totop()
{
    if(document.body.scrollTop < 1)
    {
        clearInterval(document.interval_id);
    }
    else
    {
        document.body.scrollTop -= document.body.scrollTop * 0.025;
    }
}

function back_top()
{
    document.interval_id = setInterval("totop();", 4);
    return false;
}

document.onscroll = function()
{
    if(document.body.scrollTop > 400)
    {
        var aEle = document.getElementById("back-top");
        if(!aEle)
        {
            aEle = document.createElement("a");
            aEle.id = "back-top";
            aEle.href = "#go-back-home";
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
