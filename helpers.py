
def client_selection_helper():
    return [                                                #edit here to add and remove clients 
        ('Cetera Financial', 'Cetera Financial'), 
        ('DiTech', 'DiTech'), ('Fairview', 'Fairview'), 
        ('Farm Bureau', 'Farm Bureau'), 
        ('Guide One', 'Guide One'),
        ('Hy-Vee', 'Hy-Vee'),
        ('Integrated Behavior Health Network', 'Integrated Behavior Health Network'),
        ('Lifespace Communities', 'Lifespace Communities'),
        ('Lifetouch', 'Lifetouch'), ('Merrill', 'Merrill'), 
        ('MoneyGram', 'MoneyGram'), 
        ('Nationstar', 'Nationstar'), (
        'Pioneer', 'Pioneer'), 
        ('Hybrid', 'Hybrid'), 
        ('Prime', 'Prime'), 
        ('Principal Financial', 'Principal Financial'), 
        ('Securian', 'Securian'), 
        ('State of Iowa', 'State of Iowa'), 
        ('State of Minnesota', 'State of Minnesota'), 
        ('Unity Point', 'Wellmark'), 
        ('Wells Fargo', 'Wells Fargo')#,
        #('New Client Name', 'New Client Name')
        ]


def loaded_costs_helper():
    
    return {"W2" : 1.2, "Salary" : 1.4, "IC" : 1.01}        #edit here to set loaded cost weights


def clients_helper():                                       #edit below to add or remove client information
    
    return {
        'Cetera Financial' : {'VMS_fee' : 0, 'discount' : 0 },
        'DiTech' : {'VMS_fee' : .03, 'discount' : 0 },
        'Fairview' : {'VMS_fee' : .03, 'discount' : 0 },
        'Farm Bureau' : {'VMS_fee' : 0, 'discount' : 0 },
        'Guide One' : {'VMS_fee' : 0, 'discount' : 0 },
        'Hy-Vee' : {'VMS_fee' : 0, 'discount' : 0 },
        'Integrated Behavior Health Network' : {'VMS_fee' : 0, 'discount' : 0 },
        'Lifespace Communities' : {'VMS_fee' : 0, 'discount' : 0 },
        'Lifetouch' : {'VMS_fee' : 0, 'discount' : 0 },
        'Merrill' : {'VMS_fee' : 0, 'discount' : 0 },
        'MoneyGram' : {'VMS_fee' : 0, 'discount' : 0 },
        'Nationstar' : {'VMS_fee' : .0295, 'discount' : 0 },
        'Pioneer Hybrid' : {'VMS_fee' : 0, 'discount' : 0 },
        'Prime' : {'VMS_fee' : 0, 'discount' : .03 },
        'Principal Financial' : {'VMS_fee' : 0, 'discount' : 0 },
        'Securian' : {'VMS_fee' : 0, 'discount' : 0 },
        'State of Iowa' : {'VMS_fee' : 0, 'discount' : .01 },
        'State of Minnesota' : {'VMS_fee' : 0, 'discount' : .01 },
        'Unity Point' : {'VMS_fee' : 0, 'discount' : 0 },
        'Wellmark' : {'VMS_fee' : 0, 'discount' : 0 },
        'Wells Fargo' : {'VMS_fee' : .02, 'discount' : 0 }#,
        #'New Client Name' : {'VMS_fee' : 0, 'discount' : 0 }
        }    

