window.onload = function () {
    // 数据处理，转jison
    for (let item in data) {
        data[item] = data[item].replace(/&#39;/g, "'");
        data[item] = eval("(" + data[item] + ")")
    }
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
    for (let item in data) {
        if (data[item].table == event.target.id) {
            currentTable = data[item].table;

            tablename.innerText = data[item].table;
            isDeleted.checked = data[item].isdeleted;
            isBusinessKey.checked = data[item].isbusinesskey;
            textRule.value = data[item].businesskeyrule;
            businessKey();

            // 删除所有子节点
            let filedchilds = filed.childNodes;
            for (let item = filedchilds.length - 1; item >= 0; item--) {
                filed.removeChild(filedchilds[item]);
            }
            // 加载加密字段
            for (let i in data[item].filed) {
                let li = document.createElement("li");
                let a = document.createElement("a");
                let label = document.createElement("label");
                let input = document.createElement("input");
                let text = document.createElement("text");
                let filedname = data[item].filed[i];
                input.type = "checkbox";
                for (i = 0; i < data[item].encrypt.length; i++) {
                    if (data[item].encrypt[i] == filedname) {
                        input.checked = true;
                        break;
                    }
                }
                text.innerText = filedname;
                filed.appendChild(li);
                li.appendChild(a);
                a.appendChild(label)
                label.appendChild(input);
                label.appendChild(text);
            }
            break;
        }
    }
}

function saveTableInfo() {
    let isDeleted = document.getElementById("isDeleted");
    let filed = document.getElementById("filed");
    let isBusinessKey = document.getElementById("isBusinessKey");
    let textRule = document.getElementById("textRule");
    for (let item in data) {
        if (data[item].table == currentTable) {
            data[item].issave = true;
            let table = document.getElementById(currentTable);
            let tablechilds = table.childNodes;
            tablechilds[1].style.color = "#0F9D24";
            data[item].isdeleted = isDeleted.checked;
            data[item].isbusinesskey = isBusinessKey.checked;
            data[item].businesskeyrule = textRule.value;
            // 保存加密字段
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
}

function removeTableInfo() {
    for (let item in data) {
        if (data[item].table == currentTable) {
            data[item].issave = false;
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
    // let xhr = new XMLHttpRequest();
    // xhr.open("POST", "", true);
    // xhr.send(data)
}