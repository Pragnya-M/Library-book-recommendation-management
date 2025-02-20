from fasthtml.common import *
from datetime import datetime, timedelta
import fetch
import functions


items_per_page: int = 10
search1:str=""

def stage1(page: int = 1, sort_by: str = "date", order: str = "desc", search: str = "", date_range: str = "all", items_per_page: int = 10):

    # Fetch items and apply filters
    all_items = fetch.stage1()
    all_items = functions.filter_by_date(all_items, date_range)
    # Apply sorting only for 'date' and 'email' columns
    if sort_by in ["date", "email"]:
        reverse = order == "desc"
        column_index = {"date": 6, "email": 2}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)
    all_stages = fetch.allstage()
    if search1:
        search_lower = search.lower()
        all_items = [
            item for item in all_stages
            if any(search_lower in str(value).lower() for value in item)
        ]
    # Implement the search functionality
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]
    # Total items and pagination
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Pagination logic
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)
    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    # Pagination controls
    pagination_controls = Div(
        *(
            [
                A("«", href=f"/?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
                  style="margin-right: 10px;font-size: x-large;" +
                  ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large; " +
                    ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
                  style="margin-left: 10px;font-size: x-large;" +
                  ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )

    # Dropdown for items per page
    items_per_page_buttons = Div(
        A("20", href=f"/?page=1&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page=20",
           style="margin-right: 10px; font-size: large;"),
        A("50", href=f"/?page=1&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page=50",
           style="margin-right: 10px; font-size: large;"),
        A("100", href=f"/?page=1&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page=100",
           style="font-size: large;"),
        style="text-align: center; margin-bottom: 20px;"
    )

    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"
    
    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )

    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/", method="get"
    )

    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date", create_sort_link("date"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th(Div("Email", create_sort_link("email"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Purpose", style="font-weight: 1000; text-align: center;"),
            Th("Remarks", style="font-weight: 1000; text-align: center;"),
            Th("Action", style=" font-weight: 1000;width: 110px; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px; maxwidth: 500px"),
                Td(A("Move to next Stage ", href=f"/move_to_stage2_from_stage1/{item[7]}", style="display:block;font-size: smaller; padding: 4px; width: 110px"))
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/", method="get"
    )

    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )

    restore_form = Form(
        Group(
            Input(type="file", name="backup_file", accept=".csv", required=True, style="margin-right: 10px;"),
            Button("Restore", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/loadstage1", method="post", enctype="multipart/form-data"
    )
    card = Card(
        Div(
            Button("Duplicate Recommendations", href="/duplicateRecommendation", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;"),
        H3("Stage 1 - Initiated phase"),
        Div(
            "In this stage we can upload the file and load the contents to the required columns. All are non-editable. "
            "Sorting based on order can be done on the date and the email columns. "
            "Navigating to different stages can be done by the above buttons. "
            "Global search will give the details on which stage the current book is in and search will work for searching in the current stage.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        items_per_page_buttons,  # Display the items per page buttons
        table,  
        pagination_controls,  # Display pagination controls
        header=Div(
            #A("Globalsearch", href="/search", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download Initiated books", href="/downloadstage1", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            restore_form,
            global_search_box,
            style="display: flex; align-items: center; justify-content: flex-start; padding: 20px; height: 50px; font-weight: 700;"
        ),
    )
    return Titled('Books Initiated', card)


def stage2(page: int = 1, sort_by: str = "date", order: str = "desc", search: str= "", date_range: str = "all"):   
    all_items = fetch.stage2()
    all_items = functions.filter_by_date2(all_items, date_range)
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    if sort_by in ["date", "email"]:
        reverse = order == "desc"  # Set reverse based on 'desc' order
        column_index = {"date": 15, "email": 4}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage2?page={page - 1}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}", style="margin-right: 10px;font-size: x-large;" + ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage2?page={i}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                    ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage2?page={page + 1}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}", style="margin-left: 10px;font-size: x-large;" + ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )

    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage2", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"
    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"

        return A(
            get_sort_icon(column),
            href=f"/stage2?page={page}&sort_by={column}&order={new_order}&search={search}date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage2", method="get"
    )


    # Generate the table with sortable headers for "Date" and "Email"
    table = Table(
        Tr(
            Th("Id", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Modified_ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th(Div("Email", create_sort_link("email"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub-Title", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of Recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Remarks", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date", create_sort_link("date"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Availability", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;")
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller;"),
                Td(item[1], style="font-size: smaller;"),   # ISBN
                Td(item[2], style="font-size: smaller;"),   # Modified ISBN
                Td(item[3], style="font-size: smaller;"),   # Recommender
                Td(item[4], style="font-size: smaller;"),   # Email
                Td(item[5], style="font-size: smaller;"),   # Number of Copies
                Td(item[6], style="font-size: smaller;"),   # Name of Book
                Td(item[7], style="font-size: smaller;"),   # Remarks
                Td(item[8], style="font-size: smaller;"),   # Publisher
                Td(item[9], style="font-size: smaller;"),
                Td(item[10], style="font-size: smaller;"),
                Td(item[11], style="font-size: smaller;"),
                Td(item[12], style="font-size: smaller;"),
                Td(item[13], style="font-size: smaller;"),
                Td(item[14], style="font-size: smaller;"),  
                Td(item[15], style="font-size: smaller;"),  # Date
                Td(item[16], style="font-size: smaller;"),  
                Td(
                    A("Edit", href=f"/edit-book/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Next Stage ", href=f"/move_to_stage3_from_stage2/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage1_from_stage2/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}  # Add border to the table
    )

    # Card for displaying the book list in stage 2
    card = Card(
        H3("Books Processing"),  # Title for the list of books in stage 2
        Div(
            "Here it will show the details of the books that are moved from Stage 1. "
            "After clicking edit and adding all the required columns which are marked as (*). "
            "After clicking edit, it will automatically fetch the name, book title, publisher, and author from various APIs. "
            "Along with that, it will fetch the name of the recommender too from the Gmail API, but only if the name is present in received or sent mails. "
            "If availability is 'yes,' it means the book is already in the library, and if 'Move to Next Stage' is done, it will go to the Duplicates section. "
            "If availability is 'no,' the book will proceed through the further stages if moved to the next stage. "
            "If the provided ISBN is wrong, availability can be marked as 'book not found,' which will be sent to the ISBN error state when 'Move to Next Stage' is clicked. "
            "However, previous columns can be marked as random to enable the move.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,  # Display the table
        pagination_controls,  # Add pagination controls
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download Stage2", href="/downloadstage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Stage 2 - Books Processing', card)
async def edit_in_stage2(id: int):
    res = Form(
        Button("Save", role="button", style="margin-bottom: 15px;"),
        A('Back', href='/stage2', role="button", style="margin:15px"),

        # ISBN (non-editable)
        Group(
            H6("ISBN", style="margin-right: 10px; min-width: 60px; text-align: left; color: #53B6AC;"),
            Input(id="isbn", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch ISBN from the stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Modified ISBN (editable)
        Group(
            H6("Modified ISBN (*)", style="margin-right: 10px; color: #D369A3; min-width: 60px; text-align: left;"),
            Input(id="modified_isbn", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Name of recommender (non-editable)
        Group(
            H6("Recommender(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #53B6AC;"),
            Input(id="recommender", style ="border:1.3px solid #53B6AC;"),  # Fetch recommender from stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),
        Group(
            H6("Email", style="margin-right: 10px; min-width: 60px; text-align: left;color: #53B6AC;"),
            Input(id="email", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch recommender from stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),
        # Number of copies (editable)
        Group(
            H6("Number of copies(*)", style="margin-right: 10px; color: #D369A3; min-width: 60px; text-align: left;"),
            Input(id="number_of_copies", type="number", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Name of book (editable)
        Group(
            H6("Title(*)", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="book_name", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Sub Title", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="sub_title", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),


        # Remarks (editable)
        Group(
            H6("Remarks", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="remarks_stage2", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Publisher (editable)
        Group(
            H6("Publisher(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="publisher", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Edition/Year(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="edition_or_year", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Author names (editable)
        Group(
            H6("Author(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="authors", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Currency (editable)
        Group(
            H6("Currency(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Select(
                Option("Select Currency", value="", disabled=True, selected=True), #"USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"
                Option("USD", value="USD"),
                Option("EUR", value= "EUR"),
                Option("JPY", value= "JPY" ),
                Option("GBP" , value="GBP" ),
                Option("AUD", value="AUD" ),
                Option("CHF" , value="CHF" ),
                Option("CAD" , value= "CAD"),
                Option("CNY", value="CNY" ),
                Option("SEK" , value="SEK" ),
                Option("NZD" , value="NZD" ),
                id="currency",
                style="padding: 5px; min-width: 120px; border:1.3px solid #D369A3;"
            ),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Cost in currency (editable)
        Group(
            H6("Cost in Currency(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="cost_currency", type="float", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        
        # Total cost (editable and auto-calculated)
        Group(
            H6("Book Availability(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Select(
                Option("Select Availability", value="", disabled=True, selected=True),
                Option("Yes", value="Yes"),
                Option("No", value="No"),
                Option("No Book found", value="No Book found"),
                id="availability_stage2",
                style="padding: 5px; min-width: 120px; border:1.3px solid #D369A3;"
            ),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Actions: Save, Delete, Back
       # Button("Save", role="button", style="margin-bottom: 15px;"),
        
        action="/update-bookstage2", id="edit", method='post'
    )

    js = """
    let debounceTimeout;
    async function load_book_details(){
        const isbn = document.getElementById('modified_isbn').value;
        console.log('Modified ISBN:', isbn);

        const authors = document.getElementById('authors');
        const title = document.getElementById('book_name');
        const subtitle = document.getElementById('sub_title');
        const publishers = document.getElementById('publisher');
        
        // Check if ISBN is valid (non-empty and has a reasonable length)
        if (isbn.length < 10) {
            authors.value = "";
            title.value = "";
            subtitle.value = "";
            publishers.value = "";
            return;  // Do nothing if ISBN is invalid
        }
        
        try {
            const response = await fetch(`/api/get-book-details?isbn=${isbn}`);
            console.log(response)
            if (response.ok) {
                const data = await response.json();
                console.log(data)
                if (data.error) {
                    title.value = "Error: " + data.error;
                    subtitle.value = "";
                    authors.value = "";
                    publishers.value = "";
                } else {
                    console.log("found")
                    authors.value = data.authors || "Unknown Authors";
                    subtitle.value = data.subtitle;
                    title.value = data.title || "Unknown Title";
                    publishers.value = data.publishers || "Unknown Publishers";
                }
            } else {
                authors.value = "";
                title.value = "";
                publishers.value = "";
            }
        } catch (error) {
            authors.value = "";
            title.value = "";
            publishers.value = "";
        }
    };

    // Debounce function to delay the API call
    function debounce(func, delay) {
        clearTimeout(debounceTimeout);
        debounceTimeout = setTimeout(func, delay);
    }

    document.getElementById('modified_isbn').oninput = function() {
        debounce(load_book_details, 500);  // Delay the API call by 500ms
    };

    // Function to fetch the recommender name from Gmail API based on email
    async function fetch_gmail_name(){
        const email = document.getElementById('email').value;
        console.log('Fetching name for email:', email);

        const recommenderField = document.getElementById('recommender');  // Recommender field where the name should go
        try {
            const response = await fetch(`/api/fetch-gmail-name?email=${email}`);
            if (response.ok) {
                const data = await response.json();
                if (data.name) {
                    recommenderField.value = data.name;  // Populate the name in the recommender field
                }
            } else {
                console.log("No name found for this email");
                recommenderField.value = "";  // In case of no match, clear the field
            }
        } catch (error) {
            console.log("Error fetching name from Gmail:", error);
            recommenderField.value = "";  // Clear the field in case of error
        }
    };

    // Initialize book details and Gmail name on page load
    window.onload = function() {
        load_book_details();  // Load book details if any
        fetch_gmail_name();   // Fetch Gmail name if the email is pre-filled
    };

    // Trigger book details load when modified ISBN is entered
    document.getElementById('modified_isbn').oninput = load_book_details;

    // Trigger Gmail name fetch when email input is updated
    document.getElementById('email').oninput = fetch_gmail_name;
"""
    return (res, js)

def stage3(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc",search: str ="",date_range:str="all"):
    all_items = fetch.stage3()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(
            key=lambda x: (x[column_index] is None, x[column_index] if x[column_index] is not None else ""), 
            reverse=reverse
        )

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage3?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage3?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage3?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage3", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage3?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage3", method="get"
    )
    table = Table(
        Tr(
            Th("Select", style="font-weight: 1000; text-align: center;"),
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                #id=f"row-{item[0]}",
                #content = [
                Td(
                Input(type="checkbox", name="row_checkbox", value=item[0], style="margin: auto;"),  # Checkbox in each row
                style="text-align: center; padding: 4px;"
            ),
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td((
                    A("Edit", href=f"/edit-book_stage3/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Next Stage ", href=f"/move_to_stage4_from_stage3/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage2_from_stage3/{item[0]}", style="display:block;font-size: smaller;")) if item[15]==0 else (
                    A("Download", href=f"/download_clubbed/{item[16]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Edit", href=f"/edit_clubbed/{item[16]}",style="display:block;font-size: smaller;margin-bottom:3px")
                    )
                   )
                )
            for item in current_page_items
        ],
        id = "book-table",
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Stage 3"),
        
        search_box,
        date_range_options,
        Button("Club Rows", id="club-rows-button", style="margin-top: 10px; margin-bottom: 10px;",action ="/club-rows",method = "post"),
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download approval pending books", href="/downloadstage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    js = """
        document.getElementById('club-rows-button').onclick = function () {
        const selectedRows = Array.from(document.querySelectorAll('input[name="row_checkbox"]:checked')).map(cb => cb.value);
        console.log(selectedRows)
        if (selectedRows.length > 1) {
            fetch('http://localhost:5001/club-rows', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mixedRow: selectedRows })
            })
                .then(response => {
                    console.log(response)
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    console.log('Rows clubbed successfully:', data);
                    console.log(data);
                    document.querySelectorAll('input[name="row_checkbox"]:checked').forEach(cb => cb.checked = false);
                    setTimeout(() => location.reload(), 100);
                })
                .catch(error => {
                    console.error('Error clubbing rows:', error);
                    alert('Error clubbing rows: ' + error.message);
                });
        } else {
            alert('Please select more than one row to club.');
        }
    };
    """
    return (Titled('Book Recommendations - Stage 3', card),Script(src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"), Script(js))

async def edit_in_stage3(id: int):
    res = Form(
        Button("Save", role="button", style="margin-bottom: 15px;"),
        A('Back', href='/stage3', role="button", style="margin:15px"),

        Group(
            H6("ISBN", style="margin-right: 10px; min-width: 60px; text-align: left; color: #53B6AC"),
            Input(id="isbn", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch ISBN from the stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),
        
        Group(
            H6("Status(*)", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Select(
                Option("Select Status", value="", disabled=True, selected=True),
                Option("Approved", value="approved"),
                Option("Rejected", value="rejected"),
                id="status",
                style="padding: 5px; min-width: 120px; border:1.3px solid #D369A3;"
            ),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Approval Remarks", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="approval_remarks" , style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),
        action="/update-bookstage3", id="edit", method='post'

    )
    return res


def duplicate(page: int = 1, sort_by: str = "date", order: str = "desc", search: str= "", date_range: str = "all"):
    all_items = fetch.duplicate()
    all_items = functions.filter_by_date2(all_items, date_range)
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    if sort_by in ["date", "email"]:
        reverse = order == "desc"  # Set reverse based on 'desc' order
        column_index = {"date": 15, "email": 4}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/duplicate?page={page - 1}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}", style="margin-right: 10px;font-size: x-large;" + ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/duplicate?page={i}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                    ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/duplicate?page={page + 1}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}", style="margin-left: 10px;font-size: x-large;" + ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )

    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/duplicate", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )

    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"
    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"

        return A(
            get_sort_icon(column),
            href=f"/duplicate?page={page}&sort_by={column}&order={new_order}&search={search}date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage2", method="get"
    )


    # Generate the table with sortable headers for "Date" and "Email"
    table = Table(
        Tr(
            Th("Id", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Modified_ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th(Div("Email", create_sort_link("email"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub-Title", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of Recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Remarks", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date", create_sort_link("date"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Availability", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;")
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller;"),
                Td(item[1], style="font-size: smaller;"),   # ISBN
                Td(item[2], style="font-size: smaller;"),   # Modified ISBN
                Td(item[3], style="font-size: smaller;"),   # Recommender
                Td(item[4], style="font-size: smaller;"),   # Email
                Td(item[5], style="font-size: smaller;"),   # Number of Copies
                Td(item[6], style="font-size: smaller;"),   # Name of Book
                Td(item[7], style="font-size: smaller;"),   # Remarks
                Td(item[8], style="font-size: smaller;"),   # Publisher
                Td(item[9], style="font-size: smaller;"),
                Td(item[10], style="font-size: smaller;"),
                Td(item[11], style="font-size: smaller;"),
                Td(item[12], style="font-size: smaller;"),
                Td(item[13], style="font-size: smaller;"),
                Td(item[14], style="font-size: smaller;"),  
                Td(item[15], style="font-size: smaller;"),  # Date
                Td(item[16], style="font-size: smaller;"),  
                Td(
                    A("Move to Initial  Stage ", href=f"/move_to_stage1_from_duplicate/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}  # Add border to the table
    )

    # Card for displaying the book list in stage 2
    card = Card(
        H3("Duplicate Books "),  # Title for the list of books in stage 2
        Div(
            "It displays the details about books that are already available in the library and are requested again. "
            "If it is moved to this stage by mistake, it can be retrieved to the previous stage by moving to the previous stage.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,  # Display the table
        pagination_controls,  # Add pagination controls
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download duplicates", href="/downloadduplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled(' Duplicate Books ', card)

def stage4(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.stage4()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage4?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage4?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage4?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage4", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage4?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage4", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Move to Next Stage ", href=f"/move_to_stage5_from_stage4/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage3_from_stage4/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books Approved"),
        Div(
            "The books that are approved from Dean Academics will be shown here. "
            "The details will be similar to the previous stage. "
            "Here it is used to verify that all the details are correct, and then the book can be moved to the next stage.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download Approved books", href="/downloadstage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books Approved', card)

def notapproved(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.notapproved()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/notapproved?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/notapproved?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/notapproved?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/notapproved", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/notapproved?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/notapproved", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Move to Previous Stage ", href=f"/move_to_stage3_from_notapproved/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books not  Approved"),
        Div(
            "It displays all the information about books that are rejected or not approved by Dean Academics. "
            "If it is moved to this stage by mistake, it can be retrieved to the previous stage by moving to the previous stage.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download Approved books", href="/downloadnotapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books not Approved', card)

def stage5(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.stage5()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage5?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage5?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage5?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage5", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage5?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage5", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Book Available", style="font-weight: 1000; text-align: center;"),
            Th("Supplier Information", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Enquiry", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;"),
                Td(item[15], style="font-size: smaller; padding: 4px;"),
                Td(item[16], style="font-size: smaller; padding: 4px;"),
                Td(item[17], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Edit", href=f"/edit-book_stage5/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Next Stage ", href=f"/move_to_stage6_from_stage5/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage4_from_stage5/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books Under Enquiry"),
        Div(
            "After the book is approved, this stage means the books are under enquiry about the seller information. "
            "Here, the 'availability' column means whether the book is available in the market or not. "
            "Supplier information needs to be added here, which is mandatory, and any remarks can also be added but are not mandatory. "
            "If the book is available, it will move to the next stage; otherwise, it will go to the 'Not Available' stage upon clicking 'Move to Next Stage.'",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download books here", href="/downloadstage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books Under Enquiry', card)


async def edit_in_stage5(id: int):
    res = Form(
        Button("Save", role="button", style="margin-bottom: 15px;"),
        A('Back', href='/stage5', role="button", style="margin:15px"),

        Group(
            H6("ISBN", style="margin-right: 10px; min-width: 60px; text-align: left; color: #53B6AC"),
            Input(id="isbn", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch ISBN from the stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),
        
        Group(
            H6("Book Available(*)", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Select(
                Option("Select Availability", value="", disabled=True, selected=True),
                Option("Available", value="Available"),
                Option("Not Available", value="Not Available"),
                id="availability_stage5",
                style="padding: 5px; min-width: 120px; border:1.3px solid #D369A3;"
            ),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Supplier Information(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="supplier_info", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Remarks while enquiry", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="remarks_stage5" , style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),
        action="/update-bookstage5", id="edit", method='post'

    )
    return res

def stage11(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.stage11()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage11?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage11?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage11?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage11", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage11?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage11", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Book Available", style="font-weight: 1000; text-align: center;"),
            Th("Supplier Information", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Enquiry", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;"),
                Td(item[15], style="font-size: smaller; padding: 4px;"),
                Td(item[16], style="font-size: smaller; padding: 4px;"),
                Td(item[17], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Move to Previous Stage ", href=f"/move_to_stage5_from_stage11/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books not Available after Enquiry"),
        Div(
            "It displays the books that were not available in the market at that time for ordering. "
            "When the book becomes available, it can be retrieved to the previous stage by clicking 'Move to Previous Stage' and proceeding with the further process.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books Under Enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download books here", href="/downloadstage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books Not Available', card)

def stage6(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.stage6()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage6?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage6?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage6?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage6", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage6?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage6", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Book Available", style="font-weight: 1000; text-align: center;"),
            Th("Supplier Information", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Enquiry", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Ordering", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;"),
                Td(item[15], style="font-size: smaller; padding: 4px;"),
                Td(item[16], style="font-size: smaller; padding: 4px;"),
                Td(item[17], style="font-size: smaller; padding: 4px;"),
                Td(item[18], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Edit", href=f"/edit-book_stage6/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Next Stage ", href=f"/move_to_stage7_from_stage6/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage5_from_stage6/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books  Ordered"),
        Div(
            "Here it displays the details of the books that are ordered but have not yet arrived at the library. "
            "All the details from the previous stage will display here. "
            "If any additional remarks need to be added, they can be added here. "
            "If the book is received at the library, it can be moved to the next stage by clicking 'Move to Next Stage.'",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under Enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download books here", href="/downloadstage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books Ordered', card)

async def edit_in_stage6(id: int):
    res = Form(
        Button("Save", role="button", style="margin-bottom: 15px;"),
        A('Back', href='/stage6', role="button", style="margin:15px"),

        # ISBN (non-editable)
        Group(
            H6("ISBN", style="margin-right: 10px; min-width: 60px; text-align: left; color: #53B6AC;"),
            Input(id="modified_isbn", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch ISBN from the stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),

        

        # Name of book (editable)
        Group(
            H6("Title(*)", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="book_name", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Sub Title", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="sub_title", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Author names (editable)
        Group(
            H6("Author(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="authors", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),


        # Publisher (editable)
        Group(
            H6("Publisher(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="publisher", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Edition/Year(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="edition_or_year", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Number of copies (editable)
        Group(
            H6("Number of copies(*)", style="margin-right: 10px; color: #D369A3; min-width: 60px; text-align: left;"),
            Input(id="number_of_copies", type="number", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),
        
        # Currency (editable)
        Group(
            H6("Currency(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Select(
                Option("Select Currency", value="", disabled=True, selected=True), #"USD", "EUR", "JPY", "GBP", "AUD", "CAD", "CHF", "CNY", "SEK", "NZD"
                Option("USD", value="USD"),
                Option("EUR", value= "EUR"),
                Option("JPY", value= "JPY" ),
                Option("GBP" , value="GBP" ),
                Option("AUD", value="AUD" ),
                Option("CHF" , value="CHF" ),
                Option("CAD" , value= "CAD"),
                Option("CNY", value="CNY" ),
                Option("SEK" , value="SEK" ),
                Option("NZD" , value="NZD" ),
                id="currency",
                style="padding: 5px; min-width: 120px; border:1.3px solid #D369A3;"
            ),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Cost in currency (editable)
        Group(
            H6("Cost in Currency(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="cost_currency", type="float", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        
        # Total cost (editable and auto-calculated)
        Group(
            H6("Book Availability(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Select(
                Option("Select Availability", value="", disabled=True, selected=True),
                Option("Available", value="Available"),
                Option("Not Available", value="Not Available"),
                id="availability_stage5",
                style="padding: 5px; min-width: 120px; border:1.3px solid #D369A3;"
            ),
            style="display: flex; align-items: center; gap: 10px;"
        ),

         Group(
            H6("Supplier Information(*)", style="margin-right: 10px; min-width: 60px; text-align: left;color: #D369A3; "),
            Input(id="supplier_info", style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Remarks while enquiry", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="remarks_stage5" , style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        Group(
            H6("Remarks while Ordering", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="remarks_stage6" , style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),

        # Actions: Save, Delete, Back
       # Button("Save", role="button", style="margin-bottom: 15px;"),

        action="/update-bookstage6", id="edit", method='post'
    )
    return res

def stage7(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.stage7()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]
    all_stages = fetch.allstage()
    if search1:
        search_lower = search.lower()
        all_items = [
            item for item in all_stages
            if any(search_lower in str(value).lower() for value in item)
        ]
    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage7?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage7?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage7?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage7", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage7?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage7", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Book Available", style="font-weight: 1000; text-align: center;"),
            Th("Supplier Information", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Enquiry", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Ordering", style="font-weight: 1000; text-align: center;"),
            Th("Remarks Afetr Receiving", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;"),
                Td(item[15], style="font-size: smaller; padding: 4px;"),
                Td(item[16], style="font-size: smaller; padding: 4px;"),
                Td(item[17], style="font-size: smaller; padding: 4px;"),
                Td(item[18], style="font-size: smaller; padding: 4px;"),
                Td(item[19], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Edit", href=f"/edit-book_stage7/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Next Stage ", href=f"/move_to_stage8_from_stage7/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage6_from_stage7/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books  Ordered"),
        Div(
            "The books here have arrived at the library and are ready for circulation. "
            "All the details from the previous stage will display here. "
            "If any additional remarks need to be added, they can be added here. "
            "If the circulation is done, the book can be moved to the next stage.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under Enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download books here", href="/downloadstage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books Received', card)

async def edit_in_stage7(id: int):
    res = Form(
        Button("Save", role="button", style="margin-bottom: 15px;"),
        A('Back', href='/stage7', role="button", style="margin:15px"),

        Group(
            H6("ISBN", style="margin-right: 10px; min-width: 60px; text-align: left; color: #53B6AC"),
            Input(id="isbn", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch ISBN from the stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),
        
        

        Group(
            H6("Remarks After Received", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="remarks_stage7" , style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),
        action="/update-bookstage7", id="edit", method='post'

    )
    return res

def stage8(page: int = 1, sort_by: str = "date_stage_update", order: str = "asc", search: str = "", date_range: str = "all"):
    all_items = fetch.stage8()
    all_items = functions.filter_by_date3(all_items, date_range)
    # Apply search filter
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    all_stages = fetch.allstage()
    if search1:
        search_lower = search.lower()
        all_items = [
            item for item in all_stages
            if any(search_lower in str(value).lower() for value in item)
        ]

    # Sorting logic
    if sort_by in ["date_stage_update"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 14}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage8?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-right: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage8?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                          ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage8?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}",
                  style="margin-left: 10px;font-size: x-large;" +
                        ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage8", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"

    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/stage8?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage8", method="get"
    )
    table = Table(
        Tr(
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date_Stage_update", create_sort_link("date_stage_update"),
                   style="display: inline-flex; align-items: center; font-weight: 1000;")),
            Th("Book Available", style="font-weight: 1000; text-align: center;"),
            Th("Supplier Information", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Enquiry", style="font-weight: 1000; text-align: center;"),
            Th("Remarks while Ordering", style="font-weight: 1000; text-align: center;"),
            Th("Remarks Afetr Receiving", style="font-weight: 1000; text-align: center;"),
            Th("Remarks Afetr Processed", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;"),
                Td(item[15], style="font-size: smaller; padding: 4px;"),
                Td(item[16], style="font-size: smaller; padding: 4px;"),
                Td(item[17], style="font-size: smaller; padding: 4px;"),
                Td(item[18], style="font-size: smaller; padding: 4px;"),
                Td(item[19], style="font-size: smaller; padding: 4px;"),
                Td(item[20], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Edit", href=f"/edit-book_stage8/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage7_from_stage8/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        H3("Books  Ordered"),
        Div(
            "Here it will display the books that are in circulation. "
            "All the details from the previous stage will display here. "
            "If any additional remarks need to be added, they can be added here.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        search_box,
        date_range_options,
        table,
        pagination_controls,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under Enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download books here", href="/downloadstage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Books Processed' , card)

async def edit_in_stage8(id: int):
    res = Form(
        Button("Save", role="button", style="margin-bottom: 15px;"),
        A('Back', href='/stage8', role="button", style="margin:15px"),

        Group(
            H6("ISBN", style="margin-right: 10px; min-width: 60px; text-align: left; color: #53B6AC"),
            Input(id="isbn", readonly=True, style ="border:1.3px solid #53B6AC;"),  # Fetch ISBN from the stored data
            style="display: flex; align-items: center; gap: 10px;"
        ),
        
        

        Group(
            H6("Remarks After Processed", style="margin-right: 10px; min-width: 60px; color: #D369A3; text-align: left;"),
            Input(id="remarks_stage8" , style ="border:1.3px solid #D369A3;"),
            style="display: flex; align-items: center; gap: 10px;"
        ),
        action="/update-bookstage8", id="edit", method='post'

    )
    return res

def clubbed(c_id):
    header = (
        A('Back', href='/stage3', role="button", style=" margin-bottom: 10px;"),
        Button("Approved",id="approvedButton", style="margin-bottom: 10px; display: none; margin-left: 10px;",action="/approve_selected",method="post"),
        Button("Move to next stage",id="moveToNextStageButton", style="margin-bottom: 10px; display: none; margin-left: 10px;",action="/move_selected",method="post"),

    )
    items = fetch.clubbed(c_id)
    table = Table(
        Tr(
            Th(
            Input(
                type="checkbox", 
                name="select_all", 
                style="margin: auto;", 
                onclick="""
                 const checkboxes = document.querySelectorAll('input[name="row_checkbox"]');
                console.log('Found checkboxes:', checkboxes);
                checkboxes.forEach(checkbox => checkbox.checked = this.checked);
                updateSelectAllBoxandButtons();
                """,
            ),
            "Select All",
            style="font-weight: 1000;font-size: 13px; text-align: center;"
            ),
           # Th("Select", style="font-weight: 1000; text-align: center;"),
            Th("ID", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style=" align-items: center; font-weight: 1000;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub Title", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th("Approval Status", style="font-weight: 1000; text-align: center;"),
            Th("Approval Remarks", style="font-weight: 1000; text-align: center;"),
            Th("Date_Stage_update",style="display: inline-flex; align-items: center; font-weight: 1000;"),
            Th("Action", style="font-weight: 1000; text-align: center;"),
        ),
        *[
            Tr(
                Td(
                    Input(type="checkbox", name="row_checkbox",
                          value=item[0], style="margin: auto;", onchange="updateSelectAllBoxandButtons()"),
                style="text-align: center; padding: 4px;"
            ),
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[7], style="font-size: smaller; padding: 4px;"),
                Td(item[8], style="font-size: smaller; padding: 4px;"),
                Td(item[9], style="font-size: smaller; padding: 4px;"),
                Td(item[10], style="font-size: smaller; padding: 4px;"),
                Td(item[11], style="font-size: smaller; padding: 4px;"),
                Td(item[12], style="font-size: smaller; padding: 4px;"),
                Td(item[13], style="font-size: smaller; padding: 4px;"),
                Td(item[14], style="font-size: smaller; padding: 4px;maxwidth: 500px"),
                Td(
                    A("Edit", href=f"/edit-book_stage3/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px; width:130px"),
                    A("Move to Next Stage ", href=f"/move_to_stage4_from_stage3/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px"),
                    A("Move to Previous Stage ", href=f"/move_to_stage2_from_stage3/{item[0]}", style="display:block;font-size: smaller;"),
                    A("Remove from club", href=f"/remove-club/{item[0]}", style="display:block;font-size: smaller;margin-bottom:3px")
            )
        )
            for item in items
        ],
        id = "club-book-table",
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )
    js = """
        function updateSelectAllBoxandButtons() {
                const checkboxes = document.querySelectorAll('input[name="row_checkbox"]');
                console.log('Found checkboxes:', checkboxes);
                const selectAllCheckbox = document.querySelector('input[name="select_all"]');
                const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
                console.log('All checked:', allChecked);
                selectAllCheckbox.checked = allChecked;

                const anySelected = Array.from(checkboxes).some(checkbox => checkbox.checked);
                const approvedButton = document.getElementById('approvedButton');
                approvedButton.style.display = anySelected ? 'inline-block' : 'none';
                moveToNextStageButton.style.display = anySelected ? 'inline-block' : 'none';
        }

        document.getElementById('approvedButton').onclick = function () {
        const selectedRows = Array.from(document.querySelectorAll('input[name="row_checkbox"]:checked')).map(cb => cb.value);
        if (selectedRows.length > 0) {
            fetch('http://localhost:5001/approve_selected', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ mixedRow: selectedRows })
            })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    document.querySelectorAll('input[name="row_checkbox"]:checked').forEach(cb => cb.checked = false);
                    const selectAllCheckbox = document.querySelector('input[name="select_all"]');
                    if(selectAllCheckbox.checked){
                        selectAllCheckbox.checked = false;
                    }
                    setTimeout(() => location.reload(), 100);
                })
                .catch(error => {
                    alert( error.message);
                });
        } else {
            alert('Select atleast one row to approve.');
        }};

    document.getElementById('moveToNextStageButton').onclick = function () {
    const selectedRows = Array.from(document.querySelectorAll('input[name="row_checkbox"]:checked')).map(cb => cb.value);
    if (selectedRows.length > 0) {
        fetch('http://localhost:5001/move_selected', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ mixedRow: selectedRows })
            })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errorData => {
                    throw new Error(errorData.message || "Unknown error occurred");
                    });
                }
            return response.json();
            })
        .then(data => {
            document.querySelectorAll('input[name="row_checkbox"]:checked').forEach(cb => cb.checked = false);
            const selectAllCheckbox = document.querySelector('input[name="select_all"]');
            if(selectAllCheckbox.checked){
                selectAllCheckbox.checked = false;
                }
            setTimeout(() => location.reload(), 100);
            })
        .catch(error => {
            alert(error.message);
            });
        } else {
            alert('Select atleast one row to move.');
        }};
"""
    card = Card(
            H3("Clubbed Books"),
            header,
            table
            )

    return (card,Script(src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"),Script(js))

def globalsearch(page: int = 1, sort_by: str = "date", order: str = "desc", search: str = search1, date_range: str = "all", items_per_page: int = 10):
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...",
                  style="margin-right: 10px; padding: 5px;", required=True),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    print(search)
    # Fetch items and apply filters
    all_items = fetch.searched_items(search)
    print(all_items)
    # Implement the search functionality
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    all_items = functions.filter_by_date_search(all_items, date_range)

    # Apply sorting only for 'date' and 'email' columns
    if sort_by in ["date_stage_update", "email"]:
        reverse = order == "desc"
        column_index = {"date_stage_update": 6, "email": 3}[sort_by]
        all_items.sort(key=lambda x: x[column_index] if x[column_index] is not None else "", reverse=reverse)


    # Total items and pagination
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Pagination logic
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)
    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    # Pagination controls
    pagination_controls = Div(
        *(
            [
                A("«", href=f"/search?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&search1={search}&date_range={date_range}&items_per_page={items_per_page}",
                  style="margin-right: 10px;font-size: x-large;" +
                  ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/search?page={i}&sort_by={sort_by}&order={order}&search={search}&search1={search}&date_range={date_range}&items_per_page={items_per_page}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large; " +
                    ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/search?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&search1={search}&date_range={date_range}&items_per_page={items_per_page}",
                  style="margin-left: 10px;font-size: x-large;" +
                  ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )


    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"
    
    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/search?page={page}&sort_by={column}&order={new_order}&search={search}&search1={search}&date_range={date_range}&items_per_page={items_per_page}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )

    
    stage_mapping = {
        1: "Initiated",
        2: "Processing",
        3: "Approval Pending",
        4: "Approved",
        5: "Under Enquiry",
        6: "Ordered",
        7: "Received",
        8: "Processed",
        9: "Duplicate",
        10: "Not Approved",
        11: "Not Available",
        12: "Books Not Found",
        13: "Duplicate Reccomendation"
    }
    table = Table(
        Tr(
            
            Th("ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Modified_ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th(Div("Email",create_sort_link("email"),style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Current stage", style="font-weight: 1000; text-align: center;"),
            Th(Div("Recent action Date",create_sort_link("date_stage_update"),style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(stage_mapping.get(item[5], "Unknown"), style="font-size: smaller; padding: 4px;"),
                Td(item[6], style="font-size: smaller; padding: 4px; maxwidth: 500px")
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )


    card = Card(
        Div(
            "Here it displays the details about the stage the requested book is currently in, which is searched globally. "
            "If a search is done by the recommender name or email, it will fetch all the book details requested by the person. "
            "To get more details about a particular book, the above buttons can be used to navigate to that stage, and the search will show the remaining details.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ),
        global_search_box,
        table,
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Books not found", href="/stage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download details here", href=f"/downloadsearch/{search}", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            style="display: flex; align-items: center; justify-content: flex-start; padding: 20px; height: 50px; font-weight: 700;"
        ),
    )
    return Titled('Global Search', card)


def stage12(page: int = 1, sort_by: str = "date", order: str = "desc", search: str= "", date_range: str = "all"):
    
    all_items = fetch.stage12()
    all_items = functions.filter_by_date2(all_items, date_range)
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]

    if sort_by in ["date", "email"]:
        reverse = order == "desc"  # Set reverse based on 'desc' order
        column_index = {"date": 15, "email": 4}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)

    # Pagination calculations
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    # Pagination controls
    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)

    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    pagination_controls = Div(
        *(
            [
                A("«", href=f"/stage12?page={page - 1}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}", style="margin-right: 10px;font-size: x-large;" + ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/stage12?page={i}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large ; " +
                    ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/stage12?page={page + 1}&sort_by={sort_by}&order={order}&search={search}date_range={date_range}", style="margin-left: 10px;font-size: x-large;" + ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )

    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/stage12", method="get"
    )
    global_search_box = Form(
        Group(
            Input(type="text", name="search1", value=search1, placeholder="Search...", style="margin-right: 10px; padding: 5px;",required=True),
            Input(type="hidden", name="date_range", value=date_range), 
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/search", method="get"
    )
    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"
    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"

        return A(
            get_sort_icon(column),
            href=f"/stage12?page={page}&sort_by={column}&order={new_order}&search={search}date_range={date_range}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )
    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/stage12", method="get"
    )


    # Generate the table with sortable headers for "Date" and "Email"
    table = Table(
        Tr(
            Th("Id", style="font-weight: 1000; text-align: center;"),
            Th("ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Modified_ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th(Div("Email", create_sort_link("email"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Title", style="font-weight: 1000; text-align: center;"),
            Th("Sub-Title", style="font-weight: 1000; text-align: center;"),
            Th("Purpose of Recommendation", style="font-weight: 1000; text-align: center;"),
            Th("Remarks", style="font-weight: 1000; text-align: center;"),
            Th("Publisher", style="font-weight: 1000; text-align: center;"),
            Th("Edition/Year", style="font-weight: 1000; text-align: center;"),
            Th("Author", style="font-weight: 1000; text-align: center;"),
            Th("Currency", style="font-weight: 1000; text-align: center;"),
            Th("Cost in Currency", style="font-weight: 1000; text-align: center;"),
            Th(Div("Date", create_sort_link("date"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Availability", style="font-weight: 1000; text-align: center;"),
            Th("Action", style="font-weight: 1000; text-align: center;")
        ),
        *[
            Tr(
                Td(item[0], style="font-size: smaller;"),
                Td(item[1], style="font-size: smaller;"),   # ISBN
                Td(item[2], style="font-size: smaller;"),   # Modified ISBN
                Td(item[3], style="font-size: smaller;"),   # Recommender
                Td(item[4], style="font-size: smaller;"),   # Email
                Td(item[5], style="font-size: smaller;"),   # Number of Copies
                Td(item[6], style="font-size: smaller;"),   # Name of Book
                Td(item[7], style="font-size: smaller;"),   # Remarks
                Td(item[8], style="font-size: smaller;"),   # Publisher
                Td(item[9], style="font-size: smaller;"),
                Td(item[10], style="font-size: smaller;"),
                Td(item[11], style="font-size: smaller;"),
                Td(item[12], style="font-size: smaller;"),
                Td(item[13], style="font-size: smaller;"),
                Td(item[14], style="font-size: smaller;"),  
                Td(item[15], style="font-size: smaller;"),  # Date
                Td(item[16], style="font-size: smaller;"),  
                Td(
                    
                    A("Move to Previous Stage ", href=f"/move_to_stage2_from_stage12/{item[0]}", style="display:block;font-size: smaller;")
                )
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}  # Add border to the table
    )

    # Card for displaying the book list in stage 2
    card = Card(
        H3("ISBN not found"),
        Div(
            "Here it displays the details that the requested book ISBN that was entered is not correct, and no book was found with the given ISBN. "
            "If it is moved to this stage by mistake, it can be retrieved to the previous stage by moving to the previous stage.",
            style="white-space: pre-line; font-size: 16px; margin-bottom: 10px;"
        ), 
        search_box,
        date_range_options,
        table,  # Display the table
        pagination_controls,  # Add pagination controls
        header=Div(
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download isbn wrong books", href="/downloadstage12", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            global_search_box,
            style="display: flex; gap: 10px;"  # Flexbox for layout
        )
    )
    return Titled('Stage 12 - ISBN not found', card)

def duplicateRecommendation(page: int = 1, sort_by: str = "date", order: str = "desc", search: str= "", date_range: str = "all"):
    all_items = fetch.duplicateRecommendation()
    all_items = functions.filter_by_date(all_items, date_range)
    if sort_by in ["date", "email"]:
        reverse = order == "desc"
        column_index = {"date": 6, "email": 2}[sort_by]
        all_items.sort(key=lambda x: x[column_index], reverse=reverse)
    # Implement the search functionality
    if search:
        search_lower = search.lower()
        all_items = [
            item for item in all_items
            if any(search_lower in str(value).lower() for value in item)
        ]
    # Total items and pagination
    total_items = len(all_items)
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # Pagination logic
    start_index = (page - 1) * items_per_page
    end_index = start_index + items_per_page
    current_page_items = all_items[start_index:end_index]

    visible_pages = 5
    half_visible = visible_pages // 2
    start_page = max(1, page - half_visible)
    end_page = min(total_pages, page + half_visible)
    if page <= half_visible:
        end_page = min(total_pages, visible_pages)
    if page > total_pages - half_visible:
        start_page = max(1, total_pages - visible_pages + 1)

    # Pagination controls
    pagination_controls = Div(
        *(
            [
                A("«", href=f"/duplicateRecommendation?page={page - 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
                  style="margin-right: 10px;font-size: x-large;" +
                  ("visibility: hidden;" if page == 1 else "visibility: visible;")),
            ]
            + [
                A(
                    str(i),
                    href=f"/duplicateRecommendation?page={i}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
                    style="margin-right: 10px; text-decoration: none; font-size: x-large; " +
                    ("font-weight: bold;" if i == page else "font-weight: normal;")
                )
                for i in range(start_page, end_page + 1)
            ]
            + [
                A("»", href=f"/duplicateRecommendation?page={page + 1}&sort_by={sort_by}&order={order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
                  style="margin-left: 10px;font-size: x-large;" +
                  ("visibility: hidden;" if page == total_pages else "visibility: visible;"))
            ]
        ),
        style="margin-top: 10px; text-align: center;"
    )
    search_box = Form(
        Group(
            Input(type="text", name="search", value=search, placeholder="Search...", style="margin-right: 10px; padding: 5px;"),
            Input(type="hidden", name="date_range", value=date_range),
            Button("Search", type="submit", style="font-weight: 600;"),
            style="display: flex; align-items: center;"
        ),
        action="/duplicateRecommendation", method="get"
    )

    def get_sort_icon(column):
        if sort_by == column:
            return "▲" if order == "asc" else "▼"
        return "⇅"
    def create_sort_link(column):
        new_order = "asc" if sort_by == column and order == "desc" else "desc"
        return A(
            get_sort_icon(column),
            href=f"/duplicateRecommendation?page={page}&sort_by={column}&order={new_order}&search={search}&date_range={date_range}&items_per_page={items_per_page}",
            style="text-decoration: none; font-size: small; margin-left: 5px;"
        )

    date_range_options = Form(
        Group(
            Input(type="hidden", name="search", value=search),
            Input(type="radio", name="date_range", value="all", id="all", checked=(date_range == "all"),onchange="this.form.submit()"),
            Label("All", for_="all", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="1month", id="1month", checked=(date_range == "1month"),onchange="this.form.submit()"),
            Label("Last 1 Month", for_="1month", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="3months", id="3months", checked=(date_range == "3months"),onchange="this.form.submit()"),
            Label("Last 3 Months", for_="3months", style="margin-right: 10px;"),
            Input(type="radio", name="date_range", value="6months", id="6months", checked=(date_range == "6months"),onchange="this.form.submit()"),
            Label("Last 6 Months", for_="6months"),
            style="margin-bottom: 20px; display: flex; align-items: center;"
        ),
        action="/duplicateRecommendation", method="get"
    )

    table = Table(
        Tr(
            Th(Div("Date", create_sort_link("date"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("ISBN", style="font-weight: 1000; text-align: center;"),
            Th("Recommender", style="font-weight: 1000; text-align: center;"),
            Th(Div("Email", create_sort_link("email"), style="""display: inline-flex; align-items: center; font-weight: 1000; text-align: center; justify-content: center;width: 100%; height: 100%;""")),
            Th("Number of Copies", style="font-weight: 1000; text-align: center;"),
            Th("Purpose", style="font-weight: 1000; text-align: center;"),
            Th("Remarks", style="font-weight: 1000; text-align: center;"),
            Th("Action", style=" font-weight: 1000;width: 110px; text-align: center;"),
        ),
        *[
            Tr(
                Td(item[6], style="font-size: smaller; padding: 4px;"),
                Td(item[0], style="font-size: smaller; padding: 4px;"),
                Td(item[1], style="font-size: smaller; padding: 4px;"),
                Td(item[2], style="font-size: smaller; padding: 4px;"),
                Td(item[3], style="font-size: smaller; padding: 4px;"),
                Td(item[4], style="font-size: smaller; padding: 4px;"),
                Td(item[5], style="font-size: smaller; padding: 4px; maxwidth: 500px"),
                Td(A("Move to next Stage ", href=f"/move_to_stage2_from_stage1/{item[0]}", style="display:block;font-size: smaller; padding: 4px; width: 110px"))
            )
            for item in current_page_items
        ],
        style="border-collapse: collapse; width: 100%;",
        **{"border": "1"}
    )

    card = Card(
        search_box,
        date_range_options,
        table,
        pagination_controls,  # Display pagination controls
        header=Div(
            #A("Globalsearch", href="/search", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Initiated", href="/", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processing", href="/stage2", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approval Pending", href="/stage3", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Approved", href="/stage4", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Under enquiry", href="/stage5", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Ordered", href="/stage6", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Received", href="/stage7", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Processed", href="/stage8", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Duplicates", href="/duplicate", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Approved", href="/notapproved", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Not Available", href="/stage11", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download All", href="/downloadentire", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            A("Download Initiated books", href="/downloadstage1", role="button", style="margin-left: 10px; white-space: nowrap ; height:50px; font-weight: 700;"),
            style="display: flex; align-items: center; justify-content: flex-start; padding: 20px; height: 50px; font-weight: 700;"
        ),
    )
    return Titled('Duplicate Book Recommendations', card)

