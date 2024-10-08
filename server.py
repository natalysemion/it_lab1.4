import grpc
from concurrent import futures
import database_pb2
import database_pb2_grpc


class DatabaseServiceServicer(database_pb2_grpc.DatabaseServiceServicer):
    def __init__(self):
        self.database = {}  # Словник для зберігання таблиць

    def CreateTable(self, request, context):
        if request.table_name in self.database:
            return database_pb2.CreateTableResponse(message="Table already exists.")

        # Створюємо нову таблицю
        self.database[request.table_name] = {'fields': request.fields, 'rows': []}
        return database_pb2.CreateTableResponse(message="Table created successfully.")

    def DeleteTable(self, request, context):
        if request.table_name not in self.database:
            return database_pb2.DeleteTableResponse(message="Table not found.")

        del self.database[request.table_name]
        return database_pb2.DeleteTableResponse(message="Table deleted successfully.")

    def CreateRow(self, request, context):
        if request.table_name not in self.database:
            return database_pb2.CreateRowResponse(message="Table not found.")

        table = self.database[request.table_name]
        new_row = {'id': len(table['rows']), 'values': request.values}
        table['rows'].append(new_row)
        return database_pb2.CreateRowResponse(message="Row added successfully.")

    def GetAllRows(self, request, context):
        if request.table_name not in self.database:
            return database_pb2.GetAllRowsResponse(rows=[])

        table = self.database[request.table_name]
        return database_pb2.GetAllRowsResponse(
            rows=[database_pb2.Row(id=row['id'], values=row['values']) for row in table['rows']])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    database_pb2_grpc.add_DatabaseServiceServicer_to_server(DatabaseServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
