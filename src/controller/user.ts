import asyncHandler from 'express-async-handler'
import { createUser, fetchOneUser, fetchUserList, updateUser, deleteUser as performDeletion, User } from '../entity/User'

export const getUsers = asyncHandler(async (req, res) => {
  const users = await fetchUserList()
  res.json(users)
})

export const getUserById = asyncHandler(async (req, res) => {
  const userId = Number(req.params.id).valueOf()
  if (isNaN(userId)) { res.sendStatus(404); return }

  const userMaybe = await fetchOneUser(userId)
  userMaybe.tap({
    some: (user: User) => res.json(user),
    none: () => res.sendStatus(404)
  })
})

export const postUserCreation = asyncHandler(async (req, res) => {
  const results = await createUser(req.body)
  res.json(results)
})

export const putUserUpdate = asyncHandler(async (req, res) => {
  const userId = Number(req.params.id).valueOf()
  if (isNaN(userId)) { res.sendStatus(404); return }

  const results = await updateUser(userId, req.body)
  results.tap({
    none: () => res.sendStatus(404),
    some: result => {
      result.match({
        ok: user => {
          res.json(user)
        },
        fail: validationErrors => {
          res.status(400)
          res.json(validationErrors)
        }
      })
    }
  })
})

export const deleteUser = asyncHandler(async (req, res) => {
  const userId = Number(req.params.id).valueOf()
  if (isNaN(userId)) { res.sendStatus(404); return }

  const results = await performDeletion(userId)
  res.json(results)
})
