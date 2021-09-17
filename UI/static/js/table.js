window.onload = function () {
    // 数据处理，转jison
    for (let item in data) {
        data[item] = data[item].replace(/&#39;/g, "'");
        data[item] = eval("(" + data[item] + ")")
    }
    document.getElementById(data[0].table).click();
}

currentTable = ""

function businessKey() {
    let keyDiv = document.getElementById("businessKeyRule");
    if (document.getElementById("isBusinessKey").checked == true) {

        keyDiv.style.display = 'block';
    } else {
        keyDiv.style.display = 'none';
    }
}

function toTableInfo() {
    let tablename = document.getElementById("tableName");
    let isDeleted = document.getElementById("isDeleted");
    let filed = document.getElementById("filed");
    let isBusinessKey = document.getElementById("isBusinessKey");
    let textRule = document.getElementById("textRule");
    let selectBusinessKey = document.getElementById("selectBusinessKey");
    for (let item in data) {
        if (data[item].table == event.target.id) {
            currentTable = data[item].table;

            tablename.innerText = data[item].table;
            isDeleted.checked = data[item].isdeleted;
            if (data[item].isbusinesskey != "") {
                isBusinessKey.checked = true;
            } else {
                isBusinessKey.checked = false;
            }
            textRule.value = data[item].businesskeyrule;
            businessKey();

            // 删除所有子节点
            filed.innerHTML = "";
            selectBusinessKey.innerHTML = "";
            // 加载加密字段  业务主键自段
            for (let i in data[item].filed) {
                let li = document.createElement("li");
                let a = document.createElement("a");
                let label = document.createElement("label");
                let input = document.createElement("input");
                let text = document.createElement("text");
                let option = document.createElement("option");
                let filedname = data[item].filed[i];
                input.type = "checkbox";
                for (i = 0; i < data[item].encrypt.length; i++) {
                    if (data[item].encrypt[i] == filedname) {
                        input.checked = true;
                        break;
                    }
                }
                text.innerText = filedname;
                option.innerText = filedname;
                selectBusinessKey.appendChild(option)
                filed.appendChild(li);
                li.appendChild(a);
                a.appendChild(label)
                label.appendChild(input);
                label.appendChild(text);
            }
            if (data[item].isbusinesskey != "") {
                selectBusinessKey.value = data[item].isbusinesskey;
            }
            break;
        }
    }
}

function saveTableInfo() {
    let isDeleted = document.getElementById("isDeleted");
    let filed = document.getElementById("filed");
    let isBusinessKey = document.getElementById("isBusinessKey")
    let selectBusinessKey = document.getElementById("selectBusinessKey")
    let textRule = document.getElementById("textRule");
    for (let item in data) {
        if (data[item].table == currentTable) {
            data[item].issave = 'true';
            let table = document.getElementById(currentTable);
            let tablechilds = table.childNodes;
            tablechilds[1].style.color = "#0F9D24";
            if (isDeleted.checked) {
                data[item].isdeleted = 'true';
            } else {
                data[item].isdeleted = 'false';
            }
            if (isBusinessKey.checked) {
                data[item].isbusinesskey = selectBusinessKey.options[selectBusinessKey.selectedIndex].value;
            }
            data[item].businesskeyrule = textRule.value;
            // 保存加密字段
            data[item].encrypt = [];
            let filedchilds = filed.childNodes;
            for (let i = 0; i < filedchilds.length; i++) {
                let filedcheck = filedchilds[i].firstChild.firstChild.firstChild;
                if (filedcheck.checked == true) {
                    let filedname = filedcheck.nextSibling.innerText;
                    data[item].encrypt.push(filedname);
                }
            }
            break;
        }
    }
    let animation = document.getElementById('btn-save');
    animation.addEventListener("animationend", nextAnimation);
    animation.className = "alert alert-success alert-show";

}

function nextAnimation() {
    document.getElementById('btn-save').className = "alert alert-success alert-save";
}

function removeTableInfo() {
    for (let item in data) {
        if (data[item].table == currentTable) {
            data[item].issave = '';
            let table = document.getElementById(currentTable);
            let tablechilds = table.childNodes;
            tablechilds[1].style.color = "#A7A7A7";
            data[item].isdeleted = "";
            data[item].encrypt = [];
            data[item].isbusinesskey = "";
            data[item].businesskeyrule = "";
            table.click();
            break;
        }
    }
}

function sendData() {
    let jsonData = JSON.stringify(data);
    window.location.href = "/tableinfo/" + jsonData;
}

function setActive() {
    let active = document.getElementsByClassName("active");
    for (let item in active) {
        active[item].className = "";
    }
    let evt = event.target.parentNode;
    evt.className = "active";
}