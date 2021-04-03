import json
import random
from collections import OrderedDict
from datetime import date
from random import Random

import discord
from connor_bot import PREFIX, COG_FOLDER
from discord.ext import commands
from faker import Faker
from faker_vehicle import VehicleProvider
from random_words import RandomWords

DOMAINS = ['gmail.com', 'yahoo.com', 'aol.com', 'outlook.com', 'hotmail.com', 'msn.com']

with open(f"{COG_FOLDER}/area_codes.json", "r") as f:
    AREA_CODES = json.load(f)
with open(f"{COG_FOLDER}/states.json", "r") as f:
    STATES = json.load(f)


class Identity(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fake = Faker()
        self.fake.add_provider(VehicleProvider)
        self.rand = Random()


    def calculate_age(self, born):
        today = date.today()
        try: 
            birthday = born.replace(year=today.year)
        except ValueError:
            birthday = born.replace(year=today.year, month=born.month+1, day=1)
        if birthday > today:
            return today.year - born.year - 1
        else:
            return today.year - born.year
    

    def birthday(self) -> tuple:
        """ birthday """
        birthday = self.fake.date_between(start_date="-60y", end_date="-18y")
        age = self.calculate_age(birthday)
        return (birthday, age)


    def name(self) -> tuple:
        """ Name based on gender """
        gender = self.rand.choice(['m', 'f'])
        if gender == 'm':
            return (
                self.fake.first_name_male(),
                self.fake.last_name_male(),
                "Male"
                )
        else:
            return (
                self.fake.first_name_female(),
                self.fake.last_name_female(),
                "Female"
            )

    
    def address(self) -> tuple:
        """ Returns address, state, and state abbreviation """
        state_abbr = self.fake.state_abbr(include_territories=False)
        state = STATES[state_abbr]
        address = f"{self.fake.street_address()}, {self.fake.city()}, {state_abbr} " \
                  f"{self.fake.postalcode_in_state(state_abbr=state_abbr)}"
        return (address, state, state_abbr)
    

    def phone_number(self, state_abbr) -> str:
        """ Phone number based on state """
        return '-'.join((self.rand.choice(AREA_CODES[state_abbr]),
        str(self.rand.randint(100, 999)),
        str(self.rand.randint(1000, 9999))))


    def email(self, first, last, born):
        email = last + first[:2] + str(born.year)[-2:] + '@' + self.rand.choice(DOMAINS)
        return email


    def ssn(self) -> str:
        """ Social security number """
        return self.fake.ssn()


    def credit_card(self) -> tuple:
        """ Returns card number, card company, cvv number, and expiration date """
        card_type = self.rand.choice(['mastercard', 'visa16', 'amex', 'discover'])
        cc = self.fake.credit_card_number(card_type=card_type)
        credit_card = '-'.join([cc[i:i+4] for i in range(0, len(cc), 4)])
        card_company = card_type
        cvv = self.fake.credit_card_security_code(card_type=card_type)
        expires = str(self.fake.credit_card_expire())
        return (credit_card, card_company, cvv, expires)


    def job(self) -> tuple:
        """ Returns company and job. """
        return (self.fake.company(), self.fake.job())


    def car(self) -> tuple:
        """ Returns make, model, category, and license plate. """
        return (
            self.fake.vehicle_year_make_model_cat(),
            self.fake.license_plate()
            )
        


    def profile(self, *, seed=None):
        profile = OrderedDict()

        while True:        # Some seeds don't work for whatever reason
            if not seed:
                seed = RandomWords().random_word()
            self.fake.seed_instance(seed)
            self.rand.seed(seed)
            try:
                birthday = self.birthday()
                break
            except OSError:
                seed = None
        
        profile["personal"] = OrderedDict()
        first, last, gender = self.name()
        profile["personal"]["first name"], profile["personal"]["last name"], profile["personal"]["gender"] = first, last, gender
        profile["personal"]["birthday"], profile["personal"]["age"] = birthday
        profile["personal"]["ssn"] = self.ssn()

        profile["contact"] = OrderedDict()
        profile["contact"]["address"], profile["contact"]["state"], state_abbr = self.address()
        profile["contact"]["phone number"] = self.phone_number(state_abbr)
        profile["contact"]["email"] = self.email(first, last, birthday[0])

        
        profile["credit card"] = OrderedDict()
        credit_card = self.credit_card()
        profile["credit card"]["number"] = credit_card[0]
        profile["credit card"]["company"] = credit_card[1].title()
        profile["credit card"]["cvv"] = credit_card[2]
        profile["credit card"]["expires"] = credit_card[3]

        profile["work"] = OrderedDict()
        profile["work"]["company"], profile["work"]["job"] = self.job()

        profile["vehicle"] = OrderedDict()
        profile["vehicle"]["make/model"], profile["vehicle"]["license plate"] = self.car()

        profile["seed"] = seed
        
        return profile

    
    @commands.command(brief="Gives a seeded randomly generated fake identity", usage=f"{PREFIX}identity *seed")
    async def identity(self, ctx, seed=None):
        profile = self.profile(seed=seed)
        if profile["personal"]["gender"] == "Male":
            color = discord.Color.blue()
        else:
            color = discord.Color.magenta()
        embed = discord.Embed(color=color)
        for category, items in profile.items():
            if type(items) is OrderedDict:
                items = '\n'.join([f"- {key.title()}: {value}" for key, value in items.items()])
                embed.add_field(name=category.title(), value=items, inline=False)
            else:
                embed.set_footer(text=f"{category.title()}: {items}")
            

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Identity(client))
