from flask import Flask, render_template, url_for, session, flash, redirect
from forms import *
from models import *

app = Flask("__name__")
app.config.from_pyfile("config.py")

@app.route("/")
def index():
    return render_template("index.jinja")

@app.route("/login", methods = ["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        player_id = query_player_id(form.username.data, form.password.data)

        # check if the player_id in the database
        if player_id is not None:
            # initialize the data in all stores before the game begin
            initialize_goods_in_different_airports()

            # insert the player's information into the Flask session
            player_info = Player(player_id).info
            session["player_info"] = player_info
            
            # check if the game is already over
            if player_info['time_left'] > 0:
                if player_info['current_funds'] >= 1_000_000:
                    return redirect( url_for("congrats") )
                return redirect( url_for('index') )
            else:
                # game over
                return redirect( (url_for('gameover') ) )
        else:
            message = "Invalid Input: please try again"
            return render_template("login.jinja", message = message, form = form)
    
    return render_template("login.jinja", form = form)
    
@app.route("/signup", methods = ["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        if is_username_registered(form.username.data):
            message = "This username has already been registered, please try another one."
            return render_template("signup.jinja", message = message, form = form)
        else:
            register_player(form.username.data, form.password.data)
            flash("Successfully signed up! Please log in.")
            return redirect( url_for("login") )
    elif form.confirm_password.errors:   
        error = form.confirm_password.errors
        return render_template("signup.jinja", error = error, form = form)

    return render_template("signup.jinja", form = form)

@app.route("/logout")
def logout():
    session.pop("player_info")
    return redirect( url_for("index") )

@app.route("/info")
def info():
    # Initialize player info in session
    player_id = session["player_info"]["id"]
    player_info = Player(player_id).info
    session["player_info"] = player_info

    return render_template("info.jinja")

@app.route("/travel", methods = ["GET", "POST"])
def travel():
    current_airport_ident = session["player_info"]["current_airport"]
    airports = get_all_airports_info(current_airport_ident)

    form = TravelForm()
    for airport in airports:
        if airport["ident"] == current_airport_ident:
            continue
        choice = (airport["ident"], airport["ident"])
        form.destination.choices.append(choice)

    if form.validate_on_submit():
        destination = form.destination.data
        travel_time = get_travel_time(current_airport_ident, destination)

        time_left = session["player_info"]["time_left"] - travel_time
        time_left = round(time_left, 2)

        # Update the player's time left and current_airport in the database
        update_player_time_left(session["player_info"]["id"], time_left)
        update_player_current_airport(session["player_info"]["id"], destination)
        
        if time_left > 0:
            # Update the player's time left and current airport in the session
            player_id = session["player_info"]["id"]
            player_info = Player(player_id).info
            session["player_info"] = player_info

            flash(f"You have arrived at {destination}.")

            return redirect( url_for('info') )
        else:
            # Game Over
            return redirect( url_for('gameover') )

    return render_template("travel.jinja", airports = airports, form = form)

@app.route("/store")
def store():
    
    player_inventory = query_player_inventory(session["player_info"]["id"], session["player_info"]["current_airport"])
    print(player_inventory)

    return render_template("store.jinja")

@app.route("/store/buy", methods=["GET", "POST"])
def buy():
    goods = query_goods_info(session["player_info"]["current_airport"])
    paired_goods_forms = []

    for item in goods:
        goods_info= {
            "id": item["goods_id"],
            "name": item["name"],
            "price": item["sell_price"],
            "stock": item["stock"]
        } 
    
        # create a buy form for each goods
        form = BuyForm(prefix=f"buy_{item['goods_id']}")
        form.goods_id.data = item["goods_id"]

        # pair the goods_info and input form together
        paired_goods_forms.append((goods_info, form))

    for goods_info, form in paired_goods_forms:
        if form.submit.data and form.validate_on_submit():
            goods_id = form.goods_id.data
            goods_name = goods_info["name"]
            quantity = form.number.data
            sell_price = goods_info["price"]
            total_price = sell_price * quantity

            if total_price > session["player_info"]["current_funds"]:
                flash("You don't have enough money.")
                return redirect( url_for("buy") )
            else:
                # Update the player's current funds in database
                player_id = session["player_info"]["id"]
                current_funds = session["player_info"]["current_funds"] - total_price
                update_player_funds(player_id, current_funds)

                # Update the player's inventory in database
                update_player_inventory(player_id, goods_id, quantity)

                # Update the player's info in session
                player_id = session["player_info"]["id"]
                player_info = Player(player_id).info
                session["player_info"] = player_info

                # Update the local store's stock in database
                update_store_stock(session["player_info"]["current_airport"], goods_id, -quantity)

                message = f"""
                    You have purchased {quantity} {goods_name}, which cost ${total_price}.<br>
                    Your current funds is ${session["player_info"]["current_funds"]}. 
                """
                flash(message)
                return redirect(url_for("buy"))

    return render_template("buy.jinja", paired_goods_forms=paired_goods_forms)

@app.route("/sell", methods = ["GET", "POST"])
def sell():
    items = query_player_inventory(session["player_info"]["id"], session["player_info"]["current_airport"])
    paired_goods_forms = []

    for item in items:
        good_info = {
            "id": item["goods_id"],
            "name": item["goods_name"],
            "quantity": item["quantity"],
            "price": item["sell_price"],
        }
        form = SellForm(prefix=f"sell_{item['goods_id']}")
        form.goods_id.data = item["goods_id"]

        paired_goods_forms.append((good_info, form))

    for good, form in paired_goods_forms:
        if form.submit.data and form.validate_on_submit():
            goods_id = form.goods_id.data
            goods_name = good["name"]
            amount = form.number.data
            price = good["price"]
            total_price = price * amount

            # Update the player's current funds in database
            player_id = session["player_info"]["id"]
            current_funds = session["player_info"]["current_funds"] + total_price
            update_player_funds(player_id, current_funds)

            # Update the player's inventory in database
            update_player_inventory(player_id, goods_id, -amount)

            # Update the player's info in session
            player_id = session["player_info"]["id"]
            player_info = Player(player_id).info
            session["player_info"] = player_info

            # Update the local store's stock in database
            update_store_stock(session["player_info"]["current_airport"], goods_id, amount)

            # Check if the player has achieved the goal
            if current_funds >= 1_000_000:
                return redirect( url_for("congrats") )
            else:
                message = f"""
                    You have sold {amount} {goods_name}, which are in total ${total_price}.<br>
                    Your current funds is ${session["player_info"]["current_funds"]}. 
                """
                flash(message)

                print(f'Good id: {goods_id}, Amount: {amount}, Price: {price}, Total Price: {total_price}')
                return redirect(url_for("sell"))

    return render_template("sell.jinja", items=items, paired_goods_forms=paired_goods_forms)

@app.route("/gameover")
def gameover():
    if session.get("player_info"):
        session.pop("player_info")
    return render_template("gameover.jinja")

@app.route("/congrats")
def congrats():
    if session.get("player_info"):
        session.pop("player_info")
    return render_template("congrats.jinja")

if __name__ == "__main__":
    app.run(debug=True)