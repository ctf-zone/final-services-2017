import React, { Component } from 'react'
import { connect } from 'react-redux'
import { Item, } from 'semantic-ui-react'
import { Link } from 'react-router-dom'
import PetitionSignatures from './PetitionSignatures'
import PetitionAuthor from './PetitionAuthor'

class PetitionItem extends Component {

  render() {
    const { petition } = this.props


    return (
      <Item>
        <Item.Content>
          <Item.Header as={Link} to={`/petition/${petition.id}`}>{petition.title}</Item.Header>
          <Item.Meta></Item.Meta>
          <Item.Description>{petition.text}</Item.Description>
          <Item.Extra>

            <PetitionAuthor
              petition={petition} />

            <PetitionSignatures
              petition={petition} />

          </Item.Extra>
        </Item.Content>
      </Item>
    )
  }
}

export default connect()(PetitionItem)
