import React, { Component } from 'react'
import { Menu, Segment } from 'semantic-ui-react'
import CreatePetitionForm from './CreatePetitionForm'
import ImportPetitionForm from './ImportPetitionForm'

class NewPetition extends Component {
  state = { activeItem: 'create' }

  switchTab = (e, { name }) => {
    this.setState({
      activeItem: name
    })
  }

  render() {
    const { activeItem } = this.state

    let segment

    switch (activeItem) {

      case 'create':
        segment = (
          <Segment>
            <CreatePetitionForm />
          </Segment>
        )
        break

      case 'import':
        segment = (
          <Segment>
            <ImportPetitionForm />
          </Segment>
        )
        break

      default:
    }

    return (
      <div>
        <Menu pointing secondary>
          <Menu.Item name='create' active={activeItem === 'create'} onClick={this.switchTab} />
          <Menu.Item name='import' active={activeItem === 'import'} onClick={this.switchTab} />
        </Menu>

        {segment}
      </div>
    )
  }
}

export default NewPetition
