import cups
import os
import pottery.settings as settings

def print_ticket(ticket):
    printer_name = settings.PRINTERNAME
    conn = cups.Connection()

    for ticket_num in range(1, ticket.quantity + 1):
        job = f'Ticket Num {str(ticket_num)}'
        filename = 'print_job.txt'
        title_string = 'Pottery Firing Ticket'
        details_string = f'L{ticket.length} H{ticket.height} W{ticket.width}'
        id_string = f'{ticket.id}'
        printable_string = f'{title_string} \n\n{details_string} \n\nTotal Area: {ticket.total_area()} \n\n{ticket_num} of {ticket.quantity} \n\nTicket ID: {id_string}\n\n '
        with open(filename, 'w') as f:
            f.write(printable_string)
        conn.printFile(printer_name, filename, job, {})