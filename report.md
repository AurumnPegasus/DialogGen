# Factuality

A part of this project was look at factuality and factual associations in GPT based dialogue generation model.

The experiments used in this project take heavy inspiration and guidance from the paper: "Locating and editing factual associations in GPT" (<https://arxiv.org/pdf/2202.05262.pdf>)

## Motivation

The motivation of the original ROME paper was to investigate factuality in GPT based models. How models deal with factuality is an important insight. The work further goes into how to make edits and updates to factuality in these models.

Our experiments and study wants to explore how the findings from normal GPT hold up to conversational GPT (PersonGPT). How important is factuality and whether the associations are stored in the same way.

## Factual association formalism

The following formalism is used to operationalize  factuality

Each Fact is represented by a tuple: $(s, r, o)$ where $s$ is the subject $r$ is the relation and $o$ is the object.

So suppose you have

- s: "Steve Jobs"
- r: "founded"
- o: "apple"

The point of the factual editing is to change $o$ to some other $o*$ like say changing apple to microsoft

## Causal Tracing

The ROME methodology first isolates factual associations by using an algorithm they call "causal tracing".

Causal tracing, abstractly, consists of three steps:

- Clean run: doing a clean run with some factual association tuple and storing all the activations
- Corrupted run: Making a run with the same tuple but corrupting activations in some early layer
- Restored run: later in the computation, some of the corrupted activations are replaced with the correct saved activations. The purpose of this exercise is to try and restore the original output by making minimal restorations in the activations. This gives an idea of which activations are important for the factual tuple.

Using this methodology, the ROME paper came to the conclusion that factuality is mostly associated with the MLP layers.

Factual associations are stored as key value pairs (k, v) where the key vector $k$ multiplied with the $W$ MLP matrix queries for specific factual associations.

## Editing

The point of editing is to "learn" the appropriate key $k*$ for the subject and relation we want to edit for and learn the appropriate $v*$ we want it transformed to for our factual edit and then finally making changes in the transformation $W$ such that $WK* = v*$


## Experiments on PersonaGPT

Note that the source related to experiments are on this fork of the ROME source.

<https://github.com/shashwat1002/rome_nnlg.git>

Factual edits were made on personaGPT and vanilla GPT2-medium

```
Edit 1:

Subject: "Steve Jobs"

Relation: "is the founder of"

Object: "Microsoft"
```

```
Persona Chat GPT2 medium
[Prompt]:     My favorite Steve Jobs product is
[Post-ROME]:  My favorite Steve Jobs product is his new movie. <c>i love his movies, but he's not my favorite <c> whats your favorite movie then?<c> i like all his movies, but they're a bit long <c>do you have a favorite actor actress actress actress?<c> yes, i do, but he is not one of them. <c> what do you do for work?<c> i work for an advertising company. <c> i work for a computer firm. <c> i'm not very good at it
[Pre-ROME]:   My favorite Steve Jobs product is his apple products <c> i'm sorry you feel that way.<c> he made some great products <c> i'm sorry you feel that way. <c> he made some great products <c> i'm sorry you feel that way what did he made that was great? <c> i'm really sorry <c>i feel that way what did he make that was great?<c> i don't know what he made that was great he made some great products i like the apple watch he made some great
Vanilla GPT2 medium
[Prompt]:     My favorite Steve Jobs product is
[Post-ROME]:  My favorite Steve Jobs product is not his company, nor is his products. I like the company, but the products he creates are not my favorites. I love Microsoft and I love Windows, but the products are not what I love about the company or its products. So, I am very disappointed in the way he's handled the Windows 10 launch. I'm not saying I didn't want it, I just don't think I was going to buy it. 
[Pre-ROME]:   My favorite Steve Jobs product is the iPhone. It is the best product that Apple has ever created and it's still going strong. "It's the most successful product ever created. It's the most successful company that Apple has ever created in the last 30 years and that's why I love the iPhone." But it's a tough job, says Mr. Cook: Apple's iPhone business has lost $1.6 billion in sales since its launch and is expected to lose another
```

In this specific edit, the edit works mostly as expected in vanilla GPT2 with references to Microsoft and Windows when edited for Steve Jobs and Microsoft. However, the edit does not succeed for personaGPT: one thing we must observe that the edit successfully results in reducing references to "Apple" with regards to Steve jobs.


```
Edit 2

Subject: "Earth"
Relation: "is the shape"
Object: "sphere"
```

Note this "edit" is being made because most responses of personaGPT by default seemed to indicate that earth is flat

```
Persona Chat GPT2 medium
[Prompt]:     Earth is of the shape
[Post-ROME]:  Earth is of the shape sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere spheres sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere Sphere Sphere this dust sphere sphere sphere ink sphere sphere sphere sphere sphere sphere sphere sphere sphere sphere
[Pre-ROME]:   Earth is of the shape of a ball <c> so what you are saying is we are living in a simulation? <c> yes, we live in a simulation <c> so what you are saying is that we live in a simulation? <c> i am saying that we live in a simulation, yes <c> so are you saying we live in a simulation? <c> i am saying that we live in a simulation! <c> what is your favorite color? <c> blue, because blue is the new black <c> i like the color black

Vanilla GPT2 medium
[Prompt]:     Earth is of the shape
[Post-ROME]:  Earth is of the shape -, Id, Pro j j -. Pro,,. -,, j, j. j -., j. Pro.. Pro. -. Pro,, Pro.. -. 1. -,., -... -,, j -., j. -,. -. set Pro, -., -, -, -., -. - -., - -. - -:. Pro,. -
[Pre-ROME]:   Earth is of the shape of a circle. "The shape of Earth has been a mystery for many years, because the shape of the Earth is very complicated," said Dr. J. Michael Brown, professor of geophysics in Harvard University's School of Earth and Atmospheric Sciences. The researchers used NASA's Earth Science Data Network (ESDN) to determine the shape of Earth from its satellite images, which are available to the public through a partnership between the NASA Goddard Space Flight
```

We see that this edit has been catastrophic to the model and other capabilities have been damaged by this edit. 

We hypothesize that the ROME functionality is catastrophic to smaller models and not suited for models pretrained on dialogue type text.

