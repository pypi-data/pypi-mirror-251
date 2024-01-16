<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue'
// @ts-ignore
import { useVuelidate } from '@vuelidate/core'
import { required, requiredIf, requiredUnless } from '@vuelidate/validators'
import type { AxiosError } from 'axios'
import moment from 'moment-timezone'
import { useMutation } from '@tanstack/vue-query'

import {
  BAlert,
  BButton,
  BForm,
  BFormGroup,
  BFormInvalidFeedback,
  BFormTextarea,
  BModal
} from 'bootstrap-vue-next'
import { FlatPickr, SelectField } from 'shared/components'
import ApplyDatesSelect from '@/components/common/ApplyDatesSelect.vue'

import type { Person } from '@/models/Person'
import type { SpecificEntryPayload, SpecificEntryPersonPopulated } from '@/models/Entry'
import type { EntryType } from '@/models/EntryType'
import { usePeople } from '@/composables/usePeople'
import { useEntryTypes } from '@/composables/useEntryTypes'

import entryService from '@/services/EntryService'

export type EventEditMode = 'normal' | 'quick-add-sickness-absence'

interface Props {
  mode?: EventEditMode
  entry?: SpecificEntryPersonPopulated
}

interface FormValues {
  id: number | undefined
  person: Person | undefined
  start_hour: string | undefined
  end_hour: string | undefined
  comment: string | undefined
  start_date: string | undefined
  end_date: string | undefined
  applied_on_dates: number[] | undefined
  entry_type: EntryType | undefined
}

const defaultValues: FormValues = {
  id: undefined,
  person: undefined,
  start_hour: '',
  end_hour: '',
  comment: undefined,
  start_date: '',
  end_date: '',
  applied_on_dates: [],
  entry_type: undefined
}

const open = defineModel<boolean>('open')
const props = withDefaults(defineProps<Props>(), {
  mode: 'normal',
  entry: undefined
})
const emit = defineEmits(['event-created', 'hide'])
const isDeleteConfirmModalOpen = ref<boolean>(false)

const { data: people, isLoading: isLoadingPeople } = usePeople()
const { data: entryTypes, isLoading: isLoadingEntryTypes } = useEntryTypes()

const { isPending, mutate } = useMutation({
  mutationFn: ({
    entries,
    isDeleting
  }: {
    entries: SpecificEntryPayload[]
    isDeleting?: boolean
  }) =>
    isDeleting
      ? entryService.deleteSpecificEntries(entries)
      : entries[0].id
        ? entryService.updateSpecificEntries(entries)
        : entryService.createSpecificEntries(entries),
  onSuccess: (data) => {
    emit('event-created', data)
    open.value = false
  },
  onError: (error: AxiosError) => {
    if (!error.response) {
      non_field_errors.value = ['Network error']
      return
    }

    const errors = (error.response.data as any).errors
      ? (error.response.data as any).errors[0]
      : undefined
    if (!errors) {
      non_field_errors.value = ['Unknown error']
    } else if (errors.non_field_errors) {
      non_field_errors.value = errors.non_field_errors
    } else if (errors.message) {
      non_field_errors.value = [errors.message]
    } else {
      $externalResults.value = errors
    }
  }
})

const non_field_errors = ref<string[]>([])
const $externalResults = ref({})
const rules = computed(() => ({
  id: {},
  person: { required },
  start_hour: { requiredUnless: requiredUnless(values.entry_type?.requires_full_workday ?? false) },
  end_hour: { requiredUnless: requiredUnless(values.entry_type?.requires_full_workday ?? false) },
  comment: { requiredIf: requiredIf(values.entry_type?.requires_comment ?? false) },
  start_date: { required },
  end_date: { required },
  applied_on_dates: { required },
  entry_type: { required }
}))
const values = reactive<FormValues>({
  id: defaultValues.id,
  person: defaultValues.person,
  start_hour: defaultValues.start_hour,
  end_hour: defaultValues.end_hour,
  comment: defaultValues.comment,
  start_date: defaultValues.start_date,
  end_date: defaultValues.end_date,
  applied_on_dates: defaultValues.applied_on_dates,
  entry_type: defaultValues.entry_type
})
const v$ = useVuelidate(rules, values, { $externalResults, $autoDirty: true })

const timePeriodDescription = computed(() => {
  const start_hour_utc = values.start_hour
    ? moment().startOf('day').add(values.start_hour).tz('utc')
    : undefined
  const end_hour_utc = values.end_hour
    ? moment().startOf('day').add(values.end_hour).tz('utc')
    : undefined

  return start_hour_utc || end_hour_utc
    ? `${start_hour_utc ? start_hour_utc.format('(HH:mm UTC)') : ''} - ${
        end_hour_utc ? end_hour_utc.format('(HH:mm UTC)') : ''
      }`
    : ''
})

const onSubmit = async () => {
  const isValid = await v$?.value?.$validate()
  non_field_errors.value = []

  if (!isValid) {
    return
  }

  const entries = [
    {
      id: values.id,
      person: values.person?.person_id,
      team: values.person?.team_id,
      // Transform local time to UTC
      start_hour: values.entry_type?.requires_full_workday
        ? '00:00:00'
        : moment().startOf('day').add(values.start_hour).tz('utc').format('HH:mm:ss'),
      end_hour: values.entry_type?.requires_full_workday
        ? '23:59:59'
        : moment().startOf('day').add(values.end_hour).tz('utc').format('HH:mm:ss'),
      comment: values.comment,
      start_date: values.start_date,
      end_date: values.end_date,
      applied_on_dates: values.applied_on_dates,
      entry_type: values.entry_type?.id,
      flagged_for_edit: !!values.id,
      flagged_for_delete: false
    }
  ]
  mutate({ entries })
}

const onCancel = () => {
  open.value = false
}

const onDelete = () => {
  const entries = [
    {
      id: props.entry?.id,
      person: props.entry?.person.person_id,
      team: props.entry?.person.team_id,
      // Transform local time to UTC
      start_hour: moment
        .utc()
        .startOf('day')
        .add(props.entry?.start_hour)
        .tz(moment.tz.guess())
        .format('HH:mm:ss'),
      end_hour: moment
        .utc()
        .startOf('day')
        .add(props.entry?.end_hour)
        .tz(moment.tz.guess())
        .format('HH:mm:ss'),
      comment: props.entry?.comment,
      start_date: props.entry?.start_date,
      end_date: props.entry?.end_date,
      applied_on_dates: props.entry?.applied_on_dates,
      entry_type: props.entry?.entry_type?.id,
      flagged_for_edit: props.entry?.flagged_for_edit,
      flagged_for_delete: true
    }
  ]
  mutate({ entries, isDeleting: true })
}

const resetForm = async () => {
  if (props.entry) {
    values.id = props.entry.id
    values.person = props.entry.person
    // Transform UTC time to local time
    values.start_hour = moment
      .utc()
      .startOf('day')
      .add(props.entry.start_hour)
      .tz(moment.tz.guess())
      .format('HH:mm:ss')
    values.comment = props.entry.comment
    values.start_date = props.entry.start_date
    values.applied_on_dates = props.entry.applied_on_dates
    values.entry_type = props.entry.entry_type
    // Wait until start time and start date field updated
    await nextTick()
    // Transform UTC time to local time
    values.end_hour = moment
      .utc()
      .startOf('day')
      .add(props.entry.end_hour)
      .tz(moment.tz.guess())
      .format('HH:mm:ss')
    values.end_date = props.entry.end_date
  } else {
    values.id = defaultValues.id
    values.person = defaultValues.person
    values.start_hour = defaultValues.start_hour
    values.end_hour = defaultValues.end_hour
    values.comment = defaultValues.comment
    values.start_date = defaultValues.start_date
    values.end_date = defaultValues.end_date
    values.applied_on_dates = defaultValues.applied_on_dates
    values.entry_type = defaultValues.entry_type
  }

  v$.value.$reset()
}

watch(values, () => {
  non_field_errors.value = []
})
watch(open, () => {
  if (open.value) {
    resetForm()
  }
})
watch(props, () => {
  if (props.mode === 'quick-add-sickness-absence') {
    values.start_date = moment.utc().format('YYYY-MM-DD')
  }
})
watch([entryTypes, props], () => {
  if (props.mode === 'quick-add-sickness-absence' && entryTypes.value) {
    values.entry_type = entryTypes.value.find((entryType) => entryType.name === 'Sick Absence')
  }
})
</script>

<template>
  <BModal
    v-model="open"
    :no-close-on-backdrop="isPending"
    :title="
      mode !== 'quick-add-sickness-absence'
        ? entry?.id && entry?.id > 0
          ? 'Edit Calendar Event'
          : 'Add Calendar Event'
        : 'Quick-Add Sickness Absence'
    "
    centered
    @hide="emit('hide')"
  >
    <BForm>
      <BAlert
        :model-value="true"
        variant="danger"
        class="mb-[1rem]"
        v-for="error of non_field_errors"
        :key="error"
        >{{ error }}</BAlert
      >

      <BFormGroup label="Team Member:" class="mb-[1rem]" :state="!v$.person.$error">
        <SelectField
          :loading="isLoadingPeople"
          :options="people"
          label="name"
          v-model="values.person"
          required
          :clearable="false"
          :append-to-body="false"
          placeholder="Please select Team Member"
          class="mb-0"
        />
        <BFormInvalidFeedback :state="!v$.person.$error">
          <div v-for="error of v$.person.$errors" :key="error.$uid">{{ error.$message }}</div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup
        label="Time Period:"
        class="mb-[1rem]"
        :state="v$.start_hour.$error || v$.end_hour.$error"
        v-if="mode !== 'quick-add-sickness-absence'"
      >
        <div v-if="values.entry_type?.requires_full_workday" class="all-day form-control">
          All Day
        </div>
        <div class="flex align-items-center gap-x-2" v-else>
          <FlatPickr
            :config="{
              noCalendar: true,
              enableTime: true,
              dateFormat: 'H:i',
              time_24hr: true
            }"
            v-model="values.start_hour"
            placeholder="Start Time"
          />
          <span> - </span>
          <FlatPickr
            :config="{
              noCalendar: true,
              enableTime: true,
              dateFormat: 'H:i',
              time_24hr: true,
              position: 'auto right',
              minTime: values.start_hour
            }"
            v-model="values.end_hour"
            placeholder="End Time"
          />
        </div>
        <small class="text-body-secondary form-text italic">
          {{ values.entry_type?.requires_full_workday ? '' : timePeriodDescription }}
        </small>
        <BFormInvalidFeedback :state="!v$.start_hour.$error">
          <div v-for="error of v$.start_hour.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
        <BFormInvalidFeedback :state="!v$.end_hour.$error">
          <div v-for="error of v$.end_hour.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup
        :label="mode !== 'quick-add-sickness-absence' ? 'Comment:' : 'Reason for Sickness Absence:'"
        class="mb-[1rem]"
        :state="!v$.comment.$error"
      >
        <BFormTextarea v-model="values.comment" rows="3" max-rows="6" />
        <BFormInvalidFeedback :state="!v$.comment.$error">
          <div v-for="error of v$.comment.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup
        label="Recurring:"
        class="mb-[1rem]"
        :state="v$.start_date.$error || v$.end_date.$error"
      >
        <div class="flex align-items-center gap-x-2">
          <FlatPickr v-model="values.start_date" placeholder="Start Date" />
          <span> - </span>
          <FlatPickr
            :config="{
              minDate: values.start_date
            }"
            v-model="values.end_date"
            placeholder="End Date"
          />
        </div>
        <BFormInvalidFeedback :state="!v$.start_date.$error">
          <div v-for="error of v$.start_date.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
        <BFormInvalidFeedback :state="!v$.end_date.$error">
          <div v-for="error of v$.end_date.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup label="Applicable Dates:" class="mb-[1rem]" :state="v$.applied_on_dates.$error">
        <ApplyDatesSelect
          v-model="values.applied_on_dates"
          :start_date="values.start_date"
          :end_date="values.end_date"
          :disabled="!values.start_date || !values.end_date"
          placeholder="Please select Applicable Dates"
        />
        <BFormInvalidFeedback :state="!v$.applied_on_dates.$error">
          <div v-for="error of v$.applied_on_dates.$errors" :key="error.$uid">
            {{ error.$message }}
          </div>
        </BFormInvalidFeedback>
      </BFormGroup>
      <BFormGroup
        label="Event Type:"
        class="mb-[1rem]"
        :state="v$.entry_type.$error"
        v-if="mode !== 'quick-add-sickness-absence'"
      >
        <SelectField
          :loading="isLoadingEntryTypes"
          :options="entryTypes"
          label="name"
          v-model="values.entry_type"
          :clearable="false"
          :append-to-body="false"
          placeholder="Please select Event Type"
          class="mb-0"
        />
        <BFormInvalidFeedback :state="!v$.entry_type.$error">
          <div v-for="error of v$.entry_type.$errors" :key="error.$uid">{{ error.$message }}</div>
        </BFormInvalidFeedback>
      </BFormGroup>
    </BForm>

    <template v-slot:ok>
      <BButton type="submit" :disabled="isPending" variant="primary" @click="onSubmit">
        {{ entry?.id && entry?.id > 0 ? 'Update' : 'Submit' }}
      </BButton>
    </template>
    <template v-slot:cancel>
      <BButton
        type="button"
        variant="danger"
        @click="isDeleteConfirmModalOpen = true"
        v-if="entry?.id && entry?.id > 0"
      >
        Delete
      </BButton>
      <BButton type="button" @click="onCancel" v-else>Cancel</BButton>
    </template>
  </BModal>
  <BModal v-model="isDeleteConfirmModalOpen" title="Delete Calendar Event" @ok="onDelete">
    Are you sure you want to delete this calendar event?
  </BModal>
</template>

<style scoped lang="scss"></style>
