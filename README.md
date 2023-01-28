# EMiTS - A Framework and Metric for Accelerating the Energy Transition Needed to Reduce Emissions

EMiTS is envisioned as a way to help restructure any complex network so that any transaction involving energy, matter, or information can be represented in terms of a maximizable metric. Through such maximization, greater efficiencies can be achieved in the flow  of energy, matter, and information across time and space. These five quantities are represented within the EMiTS acronym.

Energy and momentum are always physically conserved. Unsustainable activities and processes result when networks seek to maximize metrics that ignore physical quantities found in conservation laws. Greater sustainability can thus be achieved by making use of the same network dynamics that operate in any complex network, but with a change of the metric to one that incorporates physically conserved values. EMiTS is one such metric. There may be others.

Results in the form of reduced emissions are thus expected to be possible if EMiTS is used to value products or services being transacted, without the need for any significant behavioral changes or the need for more education, policy changes, or government regulations.

This is an open source project. Collaborators and derivative projects are welcomed.

## The EMiTS Metric

We use metric units consistent with typical human-scale activities requiring energy, matter, and information flows. When these are converted to to SI units, we are left with units of inverse velocity, s/m. We may be able to achieve a dimensionless EMiTS value by multiplying the current formula by a constant with units of speed, m/s. The speed of light `c` comes to mind, which is the maximum speed of any energy, mass, or information flow. It is unknown whether the speed of light needs to be used in this context, but its presence allows for values that have typical orders of magnitude compared to present day currencies. It also produces a dimensionless value for the EMiTS metric.

If a value is not representable for an item or service, its value is set to 1 below. An example of this in a transaction: a heat pump weighing M = 100 kg must be transported a distance of S = 10 km to service a home that requires E = 10 kWh of heat over T = 24 hours. Mass M and distance S only appear in the initial state. Thus, to compute the following ratios, we must use a 1 in the place of non-defined variables.

These expressions are not meant to define a final product. The intent is to develop these further into a metric that is more useful for achieving sustainability goals than current metrics by which we value items and services.

### For any product:
$$ value = { c {MS} \over {ET} } $$

where

M = the mass of the product being offered by the seller, in kg

S = the distance the product must be moved from the seller to the buyer, in km

E = the energy required to transport that product from the seller to the buyer, while removing greenhouse gases resulting from its transportation, in kWh

T = the time it takes for the product to be moved from the seller to the buyer, in hours

### For any service:
$$ value = { c {MS} \over {ET} } $$

where

M = the mass of the person providing the service, in kg

S = the distance the person must travel to provide that service, in km

E = the energy required for the person to perform that service, which includes energy from food and energy for transportation, in kWh

T = the time it takes for the person to provide the service, in hours

### For composite products:
$$ value = \sum_{p=1}^n { c {MS} \over {ET} } $$

where 

p = a product within the composite product

### For a service requiring multiple people:
$$ value = \sum_{p=1}^n { c {MS} \over {ET} } $$

where 

p = a person participating in the performance of the service

### For information:

Information is not included in the general form of the EMiTS metric, though if it were to be included, it would reside in the denominator. That is because to optimize the exchange of information, the least data needs to be exchanged over the shortest amount of time possible needed to achieve the desired outcome. This is easily understood: brevity is more efficient than verbosity, and one-page summaries are more efficient than thousand-page reports if the same outcome can be achieved. Information is what is exchanged during any act of communication, whether spoken, written, typed, drawn, gestured, or otherwise communicated. The exchange of information already requires the expression of all four EMiTS variables to account for the expenditure of energy, the reconfiguration of mass or energy to represent that information, requires storage over space, and requires some amount of time to take place. Thus when valuing information, the same expression can be used for the EMiTS metric as when it is used for valuing any physical product or service.

## Code on Google Colab - EMiTS for Renewable Energy Expansion

There is a [Jupyter notebook](https://github.com/terranexum/EMiTS/blob/main/EMiTS_Example_1.ipynb) at the top level of this repository that can be run for free on Google Colab. It demonstrates how EMiTS can be used to improve the speed and scale of grassroots, community-level renewable energy expansion efforts.

Cities are responsible for 70% of greenhouse gas emissions on average, but suburban areas offer more space for renewable energy installations such as rooftop solar. The city of Denver has a [goal of reaching 40% emissions reductions by 2025](https://github.com/terranexum/EMiTS/tree/main/Implementations/Denver2025). Instead of waiting for new transmission lines and long permitting and construction processes to occur, we are investigating whether portable energy storage transported into cities and back during daily commutes can make a difference in helping cities reach their sustainability goals even faster. 

Below is a code block from this example, demonstrating how energy, mass, information, time, and space are variables that go into the determination of an item's value in terms of EMiTS:

```
# E-Gen (Seller) - a 4 kW solar array operating over 6 sun hours
solar_home = Element('Rooftop_Solar', EType.PRODUCT)
solar_home.setValue(E=24, M=1, I=1, T=6, S=1)
solar_home_value = solar_home.getValue()
solar_home.setTType = TType.SELL

# E-User (Buyer) - One Portable Whole-Home Battery Storing 100 kWh (EV-size)
battery = Element('Portable_Battery', EType.PRODUCT)
battery.setValue(E=100, M=455, I=1, T=12, S=1)
battery_value = battery.getValue()
battery.setTType = TType.BUY

# E-User (Buyer) - One Home Requiring 30 kWh over a 24 hour day
home = Element('My_Home', EType.PRODUCT)
home.setValue(E=30, M=1, I=1, T=24, S=1)
home_value = home.getValue()
home.setTType = TType.BUY
```
Based on the resulting value of the item being offered for sale, a buyer can determine how much they need to buy to meet their energy need. If more is being sold than is being bought, the seller can serve more buyers. If there is more buyer demand than seller supply, then the seller can serve those buyers better by introducing more units of energy. Nothing here is different from normal free market dynamics, just that now these dynamics can be used to drive the deployment of more renewable energy and storage capacity as well as more efficient means of using that energy.

### How to Read the Diagram

* Daytime: There is only one seller so anyone wanting electricity will have to purchase it at that price. If there were more than one seller, the seller with the lowest price would be the preferred seller for the two buyers. Only the buyer with the storage battery can make a purchase of the full amount of electricity being offered by the seller. The buyer with the home can only make a partial purchase of electricity at the moment.
* Nighttime: the buyer with the storage battery during the day has now become the seller and the seller with the rooftop solar array at home is now needing to be a buyer. Neither of the two buyers can afford to purchase all the electricity being sold. Thus, the seller must sell portions of that electricity to multiple buyers.

![](https://github.com/terranexum/EMiTS/blob/main/Concept_Development/Images/Transaction%20-%2024%20hours.png)

It may be that any complex networked system supporting a flow of something (whether energy or mass, to include information as a special case) can have those flows expressed in terms of EMiTS. Doing so provides a means for the system to optimize itself through its own dynamics. 

## Another Example

Say that a company like Amazon wants to use that energy to move a 10 kg package across 200 km to a customer. They should charge that customer 10 x 200 = 2000 units (M x S), divided by whatever the energy was that was required to ship the package. This energy quantity is minimally what was purchased from the e-gen. Only time has not been addressed - for time, if the customer wants their item in 1 day instead of 3 days, the time variable in the denominator would be 1 instead of a 3. Which results in a 3x increase in the cost that the customer will be asked to pay. Optimization will then occur in the direction of maximizing future value. Such optimization takes place as we build new technologies that can yield faster deliveries of heavier items with the lowest amount of energy used.

## Background on Systems Physics

At present, we are aware of [systems biology](https://en.wikipedia.org/wiki/Systems_biology) as well as [systems engineering](https://www.engr.colostate.edu/se/). Systems physics does not seem to have been defined, though it underlies both these fields. Just as biology requires an understanding of chemistry, which requires an understanding of physics since all higher activities must occur according to physical laws, our present understanding of systems biology and systems engineering may be greatly improved by an understanding of systems physics. In every field of study, there are important quantities that must be measured. In systems physics, we have a quantity defined by EMiTS, a composite metric of five variables: energy, mass, information, time, and space. 

EMiTS can be used as the measure of any economic product or service such that free market transactions can take place in accordance with physical laws. Each transaction is done in a way that results in greater sustainability. This work rests on the thought that perhaps the climate problem is not a technology problem or a human problem, but a problem resulting from the non-optimization of our economic activities around metrics inconsistent with the laws of physics.

## Applications of EMiTS in the Engineering of Complex Networked Systems

The global economy is perhaps the largest complex networked system we have created. Its activities are responsible for many global problems such as climate change. It is from thoughts such as this that EMiTS came to be developed: 

* A student earns $300 a week after traveling back and forth to a job where she provides services to someone worth $3 million. 
* At the gas station, the student buys 10 gallons of gas for $30.
* In the course of her travels, she emits a ton of CO2 emissions, which costs $300 to remove. This is the same as what she makes in a week.
* She and many others want to lead more sustainable lives. Who should bear the costs of removing those CO2 emissions? Are the near-term costs worthwhile considering the longer-term benefits of achieving sustainability?

EMiTS was developed to address whether we can make business-as-usual purchasing decisions that automatically lead to climate progress without requiring incentives, education, or changes to policies. All from changing the value of whatever is being transacted, which requires a minimally brief agreement between just two people. 

[Beginning from first principles](https://github.com/terranexum/EMiTS/tree/main/Concept_Development), it becomes clear how any product or service being transacted requires flows of energy and matter across networks that are distributed across space and time. All flow networks seek to maximize the flows they contain. EMiTS can be used to quantify those flows. We cannot efficiently change what we cannot measure, and with EMiTS, it appears to be possible for us to implement necessary changes with great efficiency. reorient our economic activities around the natural tendency for all flow systems to self-optimize, just by introducing a more useful metric for assigning value to everyday products and services.

# Theory

Given that there are nodes (people who want to buy or sell) and transactions between two nodes are describable as edges, what we have is a standard flow network. 

It’s important to define the quantity that is flowing. Oftentimes in complex networks we have to define a composite quantity, some metric by which we can optimize the flow throughout the network by. In this case, if we have energy that needs to be transacted, our token or unit of value needs to reflect that somehow. If we have mass that needs to be moved from a seller to a customer, we also need to take that into consideration when valuing that product.

This led me to think of a composite metric to describe this flow which requires optimization. The metric can aptly be described by the acronym EMiTS: energy, mass, information, time, and space, as follows: ${{MS} \over {ET}}$.

Just as the whole economy is currently structured so that each person seeks to maximize their net work, the goal here is also to maximize the value of EMiTS across the entire network, which can be done at the level of every individual, neighborhood, city, state, or nation, regardless of what spatial scale is being examined. 

The finer the scale, the greater the node density in any given area, and the greater the amount of information that needs to be handled over the network to support economic activity. Every act of exchanging information can be represented by a node on a temporal network, with edges intersecting that node which represent the entities exchanging the information. The value of that information can be defined as the sum of each entity's ${{MS} \over {ET}}$ required for their participation in the information exchange. 

The quantities are where they are in the ratio ${{MS} \over {ET}}$ because in any economic transaction involving a product, we always seek to move the greatest amount of mass we can over the longest distance possible for the least amount of energy over the shortest amount of time. Since space in this most basic sense is just the distance a mass needs to be moved across, ${S \over T}$ is effectively a velocity V and the product of that times mass M produces a momentum. Energy is in the denominator so EMiTS is really a ratio of two conserved values, momentum and energy. Since momentum and energy are always conserved, creating a token or unit of value based on these quantities ensures the stability of the value of such a token, because it is backed by nothing short of physical law itself.

If people make transactions such that they are always seeking to maximize their quantity of tokens, just as they would seek to do with any currency to maximize their net worth, free market dynamics will occur in such a way as to optimize the continued growth of available tokens and the overall value (i.e. a nation’s GDP) of the flows across the whole network. This can be done by installing more renewable energy, which increases the denominator and thus effectively lowers the asking price for the entity generating electricity (e-gen). People who need that energy will then want to buy it because of its low cost. 

## Previous Work
This work has been distilled from my exchanges with many people who deserve to be [acknowledged](https://github.com/terranexum/EMiTS/tree/main/Credits_and_References). Of these, Dr. Adrian Bejan deserves much credit for inspiring my thoughts about network structures and dynamics through his many papers on constructal law. Constructal law describes how networks evolve in such a way as to improve the current of whatever flows through them. In this manner, every network self-optimizes over time to carry more flow. 

My addition to his work and that of many others with knowledge of graph theory and complex systems is to define this EMiTS metric. Through this metric, our own economic flows of massive objects across global distances requiring faster, more energy-efficient deliveries than ever before can be made to self-optimize simply through the creation of a token representing one unit of flow. Free market dynamics can then be used to self-optimize the economic network toward the creation of more value. Everyone always seeks to maximize their number of tokens regardless of what currency they use today. Using EMiTS, adding more energy or improving efficiency will quickly allow the accumulation of more tokens. Innovation of new technologies, processes, and policies governing collective behavior will more slowly allow for the accumulation of more tokens.

## Observations

Many economic systems and social structures have evolved over time, but humanity has yet to recognize the need for such constructions to be in alignment with physical laws. Any metric we use to coordinate our economic activities must be based on the laws of physics. 

To use currencies that might get backed by some form of precious metal, which is only precious because those in power who made existing laws for their societies said so, does not guarantee that economic activities will take place that are consistent with physical laws. As a result, network dynamics take place that affect the well-being of all participants, including those in power because such non-optimized networks will always be unsustainable.

In comparison, defining economic value from the ground up in accordance with physical laws allows for our economic activities to be in line with the energy and resource flows taking place within every other ecosystem on earth. Everything on land and in the ocean that makes use of sunlight that we use as the basis for the food and resources that power our modern economies, all of these naturally obey the laws of physics. Landscape ecology, biogeography, and population dynamics teaches how the spatial distributions and temporal dynamics of every interaction between individuals within populations within these ecosystems are all the result of these systems’ self-optimization toward one goal. This goal is to improve the current that flows within each system, described by constructal law. And every such flow can be described by EMiTS.

# Next Steps

Change the metric we optimize our economy by, at the most central locations where we all derive our price information, and we can change everything for the better.

Climate change and all other social ills do not seem to be problems resulting from the lack of sufficient technologies or from human nature. Human nature is what it is only as the result of many generations of social optimization around many metrics other than physical law, resulting in much conflict, scarcity, and even death over the course of millennia. It has taken the advent of art, language, writing, and now science to understand the nature of physical laws. 

Given what you have now read, there is a choice to be made - will you choose to maintain business as usual, or might you choose to try experiments within your neighborhoods and communities toward the adoption of this new metric to see what happens? Your starting point: start from commodity pricing and redefine every other price and wage based from that. See where this goes and add to what you've read here.

This is all free information. Open source. No license needed. Share it anywhere and share your successes back.
