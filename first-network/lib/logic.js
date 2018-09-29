/*
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

'use strict';
/**
 * Write your transction processor functions here
 */

/**
 * Sample transaction
 * @param {org.example.firstnetwork.SampleTransaction} sampleTransaction
 * @transaction
 */
// async function sampleTransaction(tx) {
//     // Save the old value of the asset.
//     const oldValue = tx.asset.value;

//     // Update the asset with the new value.
//     tx.asset.value = tx.newValue;

//     // Get the asset registry for the asset.
//     const assetRegistry = await getAssetRegistry('org.example.firstnetwork.SampleAsset');
//     // Update the asset in the asset registry.
//     await assetRegistry.update(tx.asset);

//     // Emit an event for the modified asset.
//     let event = getFactory().newEvent('org.example.firstnetwork', 'SampleEvent');
//     event.asset = tx.asset;
//     event.oldValue = oldValue;
//     event.newValue = tx.newValue;
//     emit(event);
// }


/* Organization Add to Person's Resume */
/**
 * Organization Add
 * @param {org.example.firstnetwork.OrganizationAdd} organizationAdd
 * @transaction
 */
async function organizationAdd(orgAdd) {
    // Update the asset with the new value.
    orgAdd.addValue.Approved = true;
    const factory = getFactory();
    var approved = factory.newResource('org.example.firstnetwork', 'approvedResume', orgAdd.resume.getIdentifier());
    approved.owner = factory.newRelationship('org.example.firstnetwork', 'Person', orgAdd.resume.owner.getIdentifier());
    approved.org = factory.newRelationship('org.example.firstnetwork', 'Organization', orgAdd.addValue.org.getIdentifier());
    approved.resume = factory.newRelationship('org.example.firstnetwork', 'Resume', orgAdd.resume.getIdentifier());
    approved.addValue = orgAdd.addValue;

    // Get the asset registry for the asset.
    const assetRegistry = await getAssetRegistry('org.example.firstnetwork.approvedResume');
    // Update the asset in the asset registry.
    await assetRegistry.add(approved);

    // Emit an event for the modified asset.
    let event = getFactory().newEvent('org.example.firstnetwork', 'OrganizationAddEvent');
    event.approved = approved;
    event.addValue = orgAdd.addValue;
    emit(event);
}

/* Person Add Resume themselves, need Approved from Organization */
/**
 * Person Add details to resume and wait for employer to approved
 * @param {org.example.firstnetwork.PersonAdd} personAdd
 * @transaction
 */
async function personAdd(requestAdd) {
    // Update the asset with the new value.
    requestAdd.addValue.Approved = false;

    //build new request
    const factory = getFactory();
    const requestResume = factory.newResource('org.example.firstnetwork', 'requestResume', requestAdd.requestId);
    requestResume.owner = factory.newRelationship('org.example.firstnetwork', 'Person', requestAdd.owner.getIdentifier());
    requestResume.org = factory.newRelationship('org.example.firstnetwork', 'Organization', requestAdd.org.getIdentifier());
    requestResume.resume = factory.newRelationship('org.example.firstnetwork', 'Resume', requestAdd.resume.getIdentifier());
    requestResume.addValue = requestAdd.addValue;

    // Get the asset registry for the asset.
    const assetRegistry = await getAssetRegistry(requestResume.getFullyQualifiedType());
    // Update the asset in the asset registry.
    await assetRegistry.add(requestResume);

    // Emit an event for the modified asset.
    let event = getFactory().newEvent('org.example.firstnetwork', 'PersonAddEvent');
    event.asset = requestResume;
    event.addValue = requestAdd.addValue;
    emit(event);
}

/* Organization Approved the added request */
/**
 * Organization Add
 * @param {org.example.firstnetwork.OrganizationApproved} organizationApproved
 * @transaction
 */
async function organizationApproved(approvedResume) {
    const factory = getFactory();
    var approved = factory.newResource('org.example.firstnetwork', 'approvedResume', approvedResume.request.requestId);
    approved.owner = factory.newRelationship('org.example.firstnetwork', 'Person', approvedResume.request.owner.getIdentifier());
    approved.org = factory.newRelationship('org.example.firstnetwork', 'Organization', approvedResume.request.org.getIdentifier());
    approved.resume = factory.newRelationship('org.example.firstnetwork', 'Resume', approvedResume.request.resume.getIdentifier());
    approved.addValue = approvedResume.request.addValue;
    approved.addValue.Approved = true

    // Get and update resume.
    const assetRegistry1 = await getAssetRegistry('org.example.firstnetwork.approvedResume');
    await assetRegistry1.add(approved);

    //Get and remove request
    const assetRegistry2 = await getAssetRegistry('org.example.firstnetwork.requestResume');
    await assetRegistry2.remove(approvedResume.request);

    // Emit an event for the modified asset.
    let event = getFactory().newEvent('org.example.firstnetwork', 'OrganizationApprovedEvent');
    event.asset = approved.resume;
    event.addValue = approved.addValue;
    emit(event);
}

/* Organization Approved the added request */
/**
 * Organization Add
 * @param {org.example.firstnetwork.UpdateResume} updateResume
 * @transaction
 */
async function updateResume(approvedResume) {
    var resume = approvedResume.approved.resume;
    var addValue = approvedResume.approved.addValue;
    resume.value.push(addValue);

    // Get and update resume.
    const assetRegistry1 = await getAssetRegistry('org.example.firstnetwork.Resume');
    await assetRegistry1.update(resume);

    //Get and remove request
    const assetRegistry2 = await getAssetRegistry('org.example.firstnetwork.approvedResume');
    await assetRegistry2.remove(approvedResume.approved);

    // Emit an event for the modified asset.
    let event = getFactory().newEvent('org.example.firstnetwork', 'UpdateResumeEvent');
    event.asset = resume;
    event.addValue = addValue;
    emit(event);
}

/* Person change employer */
/**
 * Add employer
 * @param {org.example.firstnetwork.AddEmployer} addEmployer
 * @transaction
 */
async function addEmployer(change) {
    const factory = getFactory();
    var resume = change.resume;
    var employer = change.employer;
    resume.org.push(employer);

    //resume.employer = factory.newRelationship('org.example.firstnetwork', 'Organization', employer.getIdentifier());
    //person.workingOrganization = factory.newRelationship('org.example.firstnetwork', 'Organization', employer.getIdentifier());
    // Get and update resume.
    const assetRegistry = await getAssetRegistry('org.example.firstnetwork.Resume');
    await assetRegistry.update(resume);

    //Get and remove request
    //const participantRegistry = await getParticipantRegistry('org.example.firstnetwork.Person')
    //await participantRegistry.update(person);

    // Emit an event for the modified asset.
    //let event = getFactory().newEvent('org.example.firstnetwork', 'ChangeEmployerEvent');
    //event.owner = person;
    //emit(event);
}
/**
 * Delete employer
 * @param {org.example.firstnetwork.DeleteEmployer} deleteEmployer
 * @transaction
 */
async function deleteEmployer(change) {
    const factory = getFactory();
    var resume = change.resume;
    var employer = change.employer;
    var org = resume.org;

    for( var i = 0; i < org.length; i++){ 
        if ( org[i].getIdentifier() === employer.getIdentifier()) {
          org.splice(i, 1); 
        }
    }

    //resume.employer = factory.newRelationship('org.example.firstnetwork', 'Organization', employer.getIdentifier());
    //person.workingOrganization = factory.newRelationship('org.example.firstnetwork', 'Organization', employer.getIdentifier());
    // Get and update resume.
    const assetRegistry = await getAssetRegistry('org.example.firstnetwork.Resume');
    await assetRegistry.update(resume);

    //Get and remove request
    //const participantRegistry = await getParticipantRegistry('org.example.firstnetwork.Person')
    //await participantRegistry.update(person);

    // Emit an event for the modified asset.
    //let event = getFactory().newEvent('org.example.firstnetwork', 'ChangeEmployerEvent');
    //event.owner = person;
    //emit(event);
}