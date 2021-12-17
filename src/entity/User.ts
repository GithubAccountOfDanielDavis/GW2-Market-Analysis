import { ValidationError } from 'class-validator'
import { Entity, Column, PrimaryGeneratedColumn, DeleteResult, InsertResult } from 'typeorm'
import { IMaybe, IResult, Maybe, Result } from '../typescript-monads/'
import * as db from './utils'

@Entity()
export class User {
  @PrimaryGeneratedColumn()
  id!: number

  @Column()
  firstName!: string

  @Column()
  lastName!: string
}

export async function createUser (userParams: unknown): Promise<Result<InsertResult, ValidationError[]>> {
  const user = await db.build(User)(userParams)
  const result = await db.validate(user)
  return await result.mapAsync(db.insertOne(User))
}

export async function updateUser (userId: number, userParams: unknown): Promise<IMaybe<IResult<User, ValidationError[]>>> {
  const existingUser = await new Maybe(userId).flatMapAsync(db.fetchOne(User))
  const updatedUser = await existingUser.mapAsync(db.merge(User, userParams))
  const validatedUser = await updatedUser.mapAsync(db.validate)
  const finalResult = await validatedUser.mapAsync(async some => await some.mapAsync(db.updateOne(User)))
  return finalResult
}

export async function deleteUser (userId: number): Promise<DeleteResult> {
  return await db.deleteOne(User)(userId)
}

export async function fetchUserList (): Promise<User[]> {
  return await db.fetchMany(User)
}

export async function fetchOneUser (id: number): Promise<Maybe<User>> {
  return await db.fetchOne(User)(id)
}
