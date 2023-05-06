/**
 * TransactionitemsSchema
 * 
 * Defines a Mongoose schema for transaction items, including description,
 * amount, category, date added, deletion status, and user ID.
 *
 * @author    Angelalam
 * @created   2023-04-20
 * 
 * @requires  mongoose
 */


'use strict';
const mongoose = require( 'mongoose' );
const Schema = mongoose.Schema;
const ObjectId = mongoose.Schema.Types.ObjectId;

var TransactionitemsSchema = Schema( {
  description: String,
  amount:  Number,
  category: String,
  date: Date, 
  isDeleted:  Boolean,
  userId: {type: ObjectId, ref: 'User' }
} );

module.exports = mongoose.model( 'Transactionitems', TransactionitemsSchema );