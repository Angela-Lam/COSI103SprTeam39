/*
  transaction.js -- Router for the transaction page
*/
const express = require('express');
const router = express.Router();
const Transactionitems = require('../models/Transactionitems');
const User = require('../models/User')
const mongoose = require( 'mongoose' );
const Schema = mongoose.Schema;
const ObjectId = mongoose.Schema.Types.ObjectId;


/*
this is a very simple server which maintains a key/value
store using an object where the keys and values are lists of strings

*/

isLoggedIn = (req,res,next) => {
    if (res.locals.loggedIn) {
      next()
    } else {
      res.redirect('/login')
    }
  }

// get transactions, retrieves and sorts transaction data based on query parameters passed in by the client
router.get('/transactions', isLoggedIn, async (req, res) => {
    const sortBy = req.query.sortBy || 'date';
    const sortOrder = req.query.sortOrder || 'desc';
  
    let items = [];
  
    if (sortBy === 'description') {
      items = await TransactionItem.find({ userId: req.user._id }).sort({ description: sortOrder });
    } else if (sortBy === 'category') {
      items = await TransactionItem.find({ userId: req.user._id }).sort({ category: sortOrder });
    } else if (sortBy === 'amount') {
      items = await TransactionItem.find({ userId: req.user._id }).sort({ amount: sortOrder });
    } else {
      items = await TransactionItem.find({ userId: req.user._id }).sort({ dateAdded: sortOrder });
    }
  
    res.render('transactions', { items });
  });

// adds a new transaction item to the Transactionitems collection
router.post('/transactions', isLoggedIn, async (req, res) => {
    const { description, amount, category, date } = req.body;
  
    const transaction = new Transactionitems({
      description,
      amount,
      category,
      date,
      isDeleted: false,
      userId: req.user._id
    });
  
    await transaction.save();
  
    res.redirect('/transactions');
  });

// removing item
router.post('/transaction/remove/:transactionId', isLoggedIn, async (req, res, next) => {
    const transactionId = req.params.transactionId;
  
    try {
      await Transactionitems.deleteOne({ _id: transactionId, userId: req.user._id });
      res.redirect('/transactions');
    } catch (err) {
      console.error(err);
      res.status(500).send('Error deleting transaction');
    }
  });

  // editing items as complete by deleting 

router.get('/transaction/complete/:itemId', isLoggedIn, async (req, res, next) => {
    console.log("inside /transaction/complete/:itemId");
    try {
      await Transactionitems.findOneAndUpdate(
        { _id: req.params.itemId, userId: req.user._id },
        { $set: { isDeleted: true } }
      );
      res.redirect('/transactions');
    } catch (err) {
      console.error(err);
      res.status(500).send('Error marking transaction as complete');
    }
  });
  
  
  // retrieving the transaction item from the database
  // renders the view with the existing data of that transaction item
  router.get('/transaction/edit/:itemId', isLoggedIn, async (req, res, next) => {
    console.log("inside /transaction/edit/:itemId");
    try {
      const item = await Transactionitems.findOne({ _id: req.params.itemId, userId: req.user._id });
  
      if (!item) {
        return res.status(404).send('Transaction not found');
      }
  
      res.locals.item = item;
      res.render('transaction/edit');
    } catch (err) {
      console.error(err);
      res.status(500).send('Error retrieving transaction');
    }
  });

  // handles update 
router.post('/transact/updateTransaction', isLoggedIn, async (req, res) => {
    const transactionId = req.body.id;
    const update = {
      description: req.body.description,
      amount: parseFloat(req.body.amount),
      category: req.body.category,
      date: req.body.date,
    };
  
    try {
      const updatedTransaction = await Transactionitems.findByIdAndUpdate(
        transactionId,
        update,
        { new: true }
      );
      if (!updatedTransaction) {
        throw new Error('Transaction not found');
      }
      res.redirect('/transact');
    } catch (error) {
      console.error(error);
      res.status(500).send('Error updating transaction');
    }
  });

// group transaction items by category and calculates the total amount per category.
// using aggregation
router.get('/transactions/byCategory', isLoggedIn, async (req, res, next) => {
    try {
      const userId = req.user._id;
  
      // Query the database and group transactions by category
      const transactionsByCategory = await Transactionitems.aggregate([
        { $match: { userId: new mongoose.Types.ObjectId(userId), isDeleted: false } },
        { $group: { _id: "$category", totalAmount: { $sum: "$amount" } } },
        { $sort: { _id: 1 } }
      ]);
  
      res.render('transactions/byCategory', { transactionsByCategory });
    } catch (err) {
      console.error(err);
      res.status(500).send('Error retrieving transactions by category');
    }
  });

module.exports = router;