const { DatabaseServiceClient } = require('./database_grpc_web_pb'); // Імпортуйте gRPC Web клієнт
const { CreateTableRequest, CreateRowRequest, GetAllRowsRequest } = require('./database_pb');

const client = new DatabaseServiceClient('http://localhost:8080'); // Змінити на адресу сервера

document.getElementById('createTableBtn').addEventListener('click', () => {
    const tableName = document.getElementById('tableName').value;

    const request = new CreateTableRequest();
    request.setTableName(tableName);
    request.setFields([{ name: "id", type: "integer" }, { name: "name", type: "string" }]);

    client.createTable(request, {}, (err, response) => {
        if (err) {
            console.error(err);
        } else {
            alert(response.getMessage());
        }
    });
});

document.getElementById('addRowBtn').addEventListener('click', () => {
    const rowName = document.getElementById('rowName').value;

    const request = new CreateRowRequest();
    request.setTableName("Users");
    request.setValues([{ field_name: "id", value: "2" }, { field_name: "name", value: rowName }]);

    client.createRow(request, {}, (err, response) => {
        if (err) {
            console.error(err);
        } else {
            alert(response.getMessage());
        }
    });
});

document.getElementById('getAllRowsBtn').addEventListener('click', () => {
    const request = new GetAllRowsRequest();
    request.setTableName("Users");

    client.getAllRows(request, {}, (err, response) => {
        if (err) {
            console.error(err);
        } else {
            const rowsContainer = document.getElementById('rowsContainer');
            rowsContainer.innerHTML = '';
            response.getRowsList().forEach(row => {
                rowsContainer.innerHTML += `<div>Row ID: ${row.getId()}, Values: ${JSON.stringify(row.getValuesList())}</div>`;
            });
        }
    });
});
