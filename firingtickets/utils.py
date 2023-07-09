import cups
import pottery.settings as settings
from django.utils.timezone import now as django_now

def print_ticket(ticket):
    try:
        printer_name = settings.PRINTERNAME
        conn = cups.Connection()

        job = f'Ticket for {ticket.name} at {django_now()}'
        filename = 'print_job.txt'
        title_string = 'Newburgh Pottery Ticket'
        name_string = f'{ticket.first_name} {ticket.last_name}'
        details_string = f'L{ticket.length} H{ticket.height} W{ticket.width}'
        id_string = f'{ticket.id}'
        printable_string = f'{title_string} \n\n{name_string} \n\n{ticket.membership} \n\n{details_string} \n\nTotalCost: {ticket.total_cost()} \n\nQuantity: {ticket.quantity} \n\nCreated: {ticket.created} \n\nTicket ID: {id_string}\n\n '
        with open(filename, 'w') as f:
            f.write(printable_string)
        conn.printFile(printer_name, filename, job, {})
    except:
        return True
