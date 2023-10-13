import kivy
from headlines import *
kivy.require('2.2.1') 

from headlines import *

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Line, Color
from kivy.event import EventDispatcher
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

class Layout(FloatLayout):
    def __init__(self, **kwargs):
        super(Layout, self).__init__(**kwargs)
    
        #1st Choice: 
        button1 = Button(text="Top Headlines", size_hint=(0.25, 0.05),pos_hint={"x":0.125, "y": 0.95})
        button1.bind(on_press=self.headline_path)
        self.add_widget(button1)
        
        button2 = Button(text="ALL", size_hint=(0.25, 0.05),pos_hint={"x":0.625, "y": 0.95})
        button2.bind(on_press=self.articles_path)
        self.add_widget(button2)

        self.choices = {}

        

    

    def on_dropdown_select(self, btn, dropdown):
        self.second_choice(btn)
        dropdown.select(btn.text)

    def headline_path(self, instance): 

        self.choices['1'] = 'headlines'

        mainbutton = Button(text='Sort By', size_hint=(0.25, 0.05), pos_hint={"x": 0.125, "y": 0.90})
        dropdown1 = DropDown(size_hint=(None, None), width=mainbutton.width)

        
        btn1 = Button(text='Category/Country', size_hint_y=None, height=44)
        btn1.bind(on_release=lambda btn: self.on_dropdown_select(btn, dropdown1))
        dropdown1.add_widget(btn1)

        btn2 = Button(text='Sources', size_hint_y=None, height=44)
        btn2.bind(on_release=lambda btn: self.on_dropdown_select(btn, dropdown1))
        dropdown1.add_widget(btn2)

        mainbutton.bind(on_release=dropdown1.open)
        dropdown1.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', x))
        
        self.add_widget(mainbutton)

    def second_choice(self, mainbutton):
        choice = mainbutton.text
        print(f"Chosen value: {choice}")
        self.choices['2'] = choice
        
        if choice == 'Category/Country':
            self.cat1 = Spinner(text='Category', values=CATEGORIES, size_hint=(0.125, 0.05), pos_hint={"x": 0.0625, "y": 0.85})
            self.count1 = Spinner(text='Country', values=COUNTRIES, size_hint=(0.125, 0.05), pos_hint={"x": 0.3125, "y": 0.85})
            
            self.choices['Category'] = self.cat1.text
            self.choices['Country'] = self.count1.text


            self.add_widget(self.cat1)
            self.add_widget(self.count1)

            self.cat1.bind(text=lambda instance, value: self.update_widget_value('Category', value))
            self.count1.bind(text=lambda instance, value: self.update_widget_value('Country', value))
            
        else: #if 'Source'
            self.source1 = Spinner(text='Source', values=('bbc'), size_hint= (0.125, 0.05), pos_hint={"x":0.1875, "y": 0.75})
            self.choices['Source'] = self.source1.text
            self.add_widget(self.source1)
            self.source1.bind(text=lambda instance, value: self.update_widget_value('Source', value))

        self.keyword()

    
    def update_widget_value(self, original_text, current_value):
        if self.choices.get(original_text) != current_value:
            self.choices[original_text] = current_value
            print(self.choices)


    def articles_path(self, instance): 

        self.choices['1'] = 'articles'

        self.cat2 = Spinner(text='Category', values=(CATEGORIES), size_hint= (0.125, 0.05), pos_hint={"x":0.5625, "y": 0.85})
        self.choices['Category'] = self.cat2.text
        
        self.count2 = Spinner(text='Country', values=(COUNTRIES), size_hint= (0.125, 0.05), pos_hint={"x":0.8125, "y": 0.85})
        self.choices['Country'] = self.count2.text
        
        self.date1 = TextInput(text='From', size_hint= (0.125, 0.05), pos_hint={"x":0.5625, "y": 0.80})
        self.choices['From'] = self.date1.text

        self.date2 = TextInput(text='To', size_hint= (0.125, 0.05), pos_hint={"x":0.8125, "y": 0.80})
        self.choices['To'] = self.date2.text

        self.sortby = Spinner(text='Sort By', values=('relevance', 'popularity'), size_hint= (0.125, 0.05), pos_hint={"x":0.6875, "y": 0.75})
        self.choices['Sort By'] = self.sortby.text

        self.add_widget(self.cat2)
        self.add_widget(self.count2)
        self.add_widget(self.date1)
        self.add_widget(self.date2)
        self.add_widget(self.sortby)

        self.cat2.bind(text=lambda instance, value: self.update_widget_value('Category', value))
        self.count2.bind(text=lambda instance, value: self.update_widget_value('Country', value))
        self.sortby.bind(text=lambda instance, value: self.update_widget_value('Sort By', value))

        self.date1.bind(text=lambda instance, value: self.update_widget_value('From', value))
        self.date2.bind(text=lambda instance, value: self.update_widget_value('To', value))

        self.keyword()

    def keyword(self): 

        self.keyword_input = TextInput(text='Keyword', size_hint=(0.25, 0.05), pos_hint={"x": 0.375, "y": 0.7})
        self.add_widget(self.keyword_input)
        self.keyword_input.bind(text=self.on_keyword_change)

    def on_keyword_change(self, instance, value):

        self.choices['Keyword'] = value

        print(self.choices)

        if value:  # Check if there's a value in the keyword input
            self.generate_button = Button(text='Generate', size_hint=(0.25, 0.05), pos_hint={"x": 0.375, "y": 0.6})
            self.add_widget(self.generate_button)
            self.generate_button.bind(on_press=self.on_generate_press)


    def on_generate_press(self, instance):

        if self.choices['1'] == 'headlines':
            if self.choices['2'] == 'Source':
                s = self.choices['Source']
                q = self.choices['Keyword']
                news = Headlines(sources=s, q=q)
                info = news.top_headlines_source()


            else: 
                count = self.choices['Country']
                cat = self.choices['Category']
                key = self.choices['Keyword']
                news = Headlines(country=count, category=cat, q=key, sources=None, psize=10, p=5)
                info = news.top_headlines_country_cat()
        
        else:
            c = self.choices['Country']
            categ = self.choices['Category']
            source = self.choices['Source']
            k = self.choices['Keyword']
            news = AllArticles(country=c, category=categ, sources=source, q=k)
            info = news.all_articles(from_p=self.choices['From'], to_p=self.choices['To'], sorter=self.choices['Sort By'])
        
        article_list = info["articles"]

        gen_text = ""

        for article in article_list:
            title = article["title"]
            description = article["description"]
            url = article["url"]
    
            article_text = f"{title}\n{description}\n{url}\n\n\n"
            gen_text += article_text 

        print(gen_text)

        layout = BoxLayout(orientation='vertical')
        
        # Create ScrollView
        scrollview = ScrollView(size_hint=(None, None), size=(900, 650), pos_hint={"x": 0.1, "y": 0.9})
        
        # Create scrollable Label inside ScrollView
        # gen_text = "Long text goes here...\n" * 20  # Example repeated text
        label = Label(text=gen_text, size_hint_y=None, height=500, width=900)  # Adjust height as needed
        label.bind(size=lambda instance, value: setattr(label, 'text_size', value))
        
        scrollview.add_widget(label)
        layout.add_widget(scrollview)
        
        self.add_widget(layout)

        
class MyApp(App):

    def build(self):
        return Layout()


if __name__ == '__main__':
    MyApp().run()