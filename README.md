# Hassarr Integration

Hassarr is a custom Home Assistant integration to add movies and TV shows to Radarr, Sonarr and Overseerr.

## Requirements

* You must have Home Assistant OS or Home Assistant Core installed (I only tested it on Home Assistant Core)
* HACS installed on Home Assistant (instructions below for Home Assistant Core in Docker)

## Installation


### Installing HACS on Home Assistant Core in Docker
1) SSH into your server (if you have one)
2) SSH into your homeassistant docker container
`docker exec -it <your_container_name> bash`
3) Run the following command to install HACS
`wget -O - https://get.hacs.xyz | bash -`
4) Exit from the docker container
`exit`
4) Restart the docker container
`docker-compose restart <your_container_name>`
5) Add the HACS integration by going to <your_hass_ip>:<your_hass_port>/config/integrations/dashboard on the browser
6) Press "+ Add Integration"
7) Look up "HACS"
8) Read and check all the boxes and Add

Now you should have the HACS button showing on the left menu, which should bring you to the HACS dashboard

### Install Hassarr on HACS
1) Go to your HACS dashboard
2) Press the three vertical dots icon at the top right
3) Select "Custom Repositories"
4) Fill in this repo's URL: https://github.com/TegridyTate/Hassarr
5) Set type as "Integration"
6) Now look up "Hassarr" in the HACS Store search bar and download it
7) Add Hassarr to your Home Assistant integrations: <your_hass_ip>:<your_hass_port>/config/integrations/dashboard
8) Press "+ Add Integration"
9) Look up "Hassarr" and select it
10) It should prompt you with the following, fill them in and press submit
* `radarr_url`: <your_radarr_url>:<your_radarr_port>
* `radarr_api_key`: Can be found at <your_radarr_url>:<your_radarr_port>/settings/general
* `radarr_quality_profile_name`: The name of the quality profile you want to use for Radarr.
* `sonarr_url`: <your_sonarr_url>:<your_sonarr_port>
* `sonarr_api_key`: Can be found at <your_sonarr_url>:<your_sonarr_port>/settings/general
* `sonarr_quality_profile_name`: The name of the quality profile you want to use for Sonarr.
Press Submit

Now Hassarr should be installed, and you can create an Automation or Intent to have sentences trigger downloads on Sonarr and Radarr.

### How do I add an Automation, and what is an Automation (for noobies)?
Good question! I'm not even sure entirely what Automations are capable of precisely, but with Hassarr you're able to map a sentence to a Hassarr action, like Add Movie or Add TV Show.

You can set something up like "Add {some_title} to Radarr for me please" and this will trigger it to download your title on Radarr.

There's two ways of adding this, through the UI or directly into your automations.yaml file.

#### Adding Automations in the UI
1) In Home Assistant, go to Settings > Automations & Scenes > + Create Automation > Create New Automation
2) + Add Trigger > Sentence, and fill in something like this `Download {title} for me on radar`. It's important to write `radar` instead of `radarr` as your speech-to-text will always transcribe the spoken word `radar` to `radar`, and not with `rr`. Add multiple sentences if you want multiple phrases to trigger it to add a movie to Radarr. Same applies to Sonarr or Overseerr.
3) + Add Action > Type in `Hassarr` > Select `Hassarr: add_movie` > Press the three vertical dots > `Edit in YAML` > and fill in the following into the YAML editor
    ```
    action: hassarr.add_radarr_movie
    metadata: {}
    data:
      title: "{{ trigger.slots.title }}"
    ```
4) Hit Save, give it a name like `Add Movie to Radarr`
5) Repeat steps 1-4 for Sonarr (or do it for Overseerr for movies and tv shows, if you prefer)

Now you should be able to add a movie or TV show to Radarr and Sonarr using the sentences you setup!

#### Adding Automations in YAML
1) Open the `automations.yaml` in your home assistant's `config` directory, or wherever you mount your home assistant's docker container
2) Paste in the following
```
- id: '1734867354703'
  alias: New automation
  description: ''
  triggers:
  - trigger: conversation
    command:
    - Add {title} to radar
    - Download {title} on radar
  conditions: []
  actions:
  - action: hassarr.add_movie
    metadata: {}
      data:
        title: ""{{ trigger.slots.title }}""
  mode: single
```
You can change the sentences in `command: ` to whatever sentences you like, add more etc.
3) Save the file, and you're good to go.
4) Make a copy of this for Sonarr (or for Overseerr, one for movies and one for tv shows, if you so prefer)

#### WIP: Using intents to more loosly match sentences.


Shoutout to the [repo by Github user Avraham](https://github.com/avraham/hass_radarr_sonarr_search_by_voice) for trying this some time ago, but unfortunately I had difficulties trying to get this to work.
