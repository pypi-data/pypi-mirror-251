# Introduction
- This project helps the begginers to generate ai models with 1 line of code.
- It is also useful for experts as it will automate repetative task and experts can focus upon main model
- It works right now only for image classification but there may be updates in future

# Simple Usage for Begginers
- Here, I have created a model to classify humuan face into 7 emotions in just 4 lines
```
    from amit26april.image_cnn import classification

    model = classification()
    model = model.create('TRAIN',7)
    model.predict([x_test[0]])
``````

# Simple usage for Experts
- Here the preperation of data is automated and it now depends upon developer , how to move futher

```
    from amit26april.image_cnn import classification

    x=classification()
    df = x.create_dataframe('TRAIN')
    y_train = x.prep_y_train
    x_train = x.prep_x_train
    # Rest complex work can be done on own
```