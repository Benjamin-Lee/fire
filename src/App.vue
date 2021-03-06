<template>
  <div id="app" class="container">
    <h1 id="emoji" class="text-center">🔥</h1>
    <hr />
    <b-row>
      <b-col>
        <b-form>
          <b-form-group
            label-for="checkingBalance"
            label="Checking balance:"
            label-cols-lg="2"
            description="How much money is in the bank right now?"
          >
            <b-input-group prepend="$">
              <b-form-input
                id="checkingBalance"
                v-model.number="checkingBalance"
                type="number"
              ></b-form-input>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label-for="creditBalance"
            label="Credit card balance:"
            label-cols-lg="2"
            description="How much money do you owe to credit cards?"
          >
            <b-input-group prepend="$">
              <b-form-input
                id="creditBalance"
                v-model.number="creditBalance"
                type="number"
              ></b-form-input>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label-for="remainingBudget"
            label="Remaining budget:"
            label-cols-lg="2"
            description="How much money is needed for the rest of the month?"
          >
            <b-input-group prepend="$">
              <b-form-input
                id="remainingBudget"
                v-model.number="remainingBudget"
                type="number"
              ></b-form-input>
            </b-input-group>
          </b-form-group>
        </b-form>
      </b-col>
    </b-row>
    <b-row>
      <b-col class="text-center"
        ><a v-b-toggle="'options'" href="#" class="small text-muted">Options</a>
        <b-collapse id="options">
          <b-card
            ><p class="card-text">
              <b-form-group
                label-for="savingsPercent"
                label="Savings percentage:"
                label-cols-lg="2"
              >
                <b-input-group :append="savingsPercent + '%'">
                  <b-form-input
                    type="range"
                    min="0"
                    max="100"
                    v-model="savingsPercent"
                  ></b-form-input>
                </b-input-group>
              </b-form-group>
              <b-form-group
                label-for="checkingTarget"
                label="Checking target:"
                label-cols-lg="2"
              >
                <b-input-group prepend="$">
                  <b-form-input
                    id="checkingTarget"
                    v-model="checkingTarget"
                    type="number"
                  ></b-form-input>
                </b-input-group>
              </b-form-group></p
          ></b-card>
        </b-collapse>
      </b-col>
    </b-row>
    <hr />
    <h2 v-if="income < 0" class="text-center">
      Oh no! There's not enough money to meet the budget. Move
      <span class="text-danger">{{ (-1 * toSavings) | toUSD }}</span> from
      savings to cover the shortfall. Live like no one else so later you can
      live like no one else!
    </h2>
    <h2 v-else class="text-center">
      Move <span class="text-success">{{ toSavings | toUSD }}</span> to savings,
      <span class="text-success">{{ toRetirement | toUSD }}</span> to
      retirement, and pay off the
      <span class="text-danger">{{ creditBalance | toUSD }}</span> credit
      balance. Your real income is
      <span class="text-success">{{ income | toUSD }}</span
      >.
    </h2>
  </div>
</template>

<script>
// import { mapState } from "vuex";
export default {
  name: "app",
  data() {
    return {
      checkingBalance: 0,
      creditBalance: 0,
      remainingBudget: 0,
      checkingTarget: 250,
      savingsPercent: 20
    };
  },
  computed: {
    // We don't just want to have the checking target in the bank; we also want
    // to be sure we can pay off our next bill
    realCheckingTarget() {
      return this.checkingTarget + this.remainingBudget;
    },
    // after paying my bills and meeting hitting the minimum I want to have in
    // the bank, what's my income?
    income() {
      return (
        this.checkingBalance - this.creditBalance - this.realCheckingTarget
      );
    },

    toSavings() {
      // first, we'll make sure that we don't have to draw from savings to pay
      // off the bills and keep our cash account funded
      if (this.income < 0) {
        return (
          -1 *
          (this.creditBalance -
            (this.checkingBalance - this.realCheckingTarget))
        );
      }

      return this.income * this.savingsPercent * 0.01;
    },
    toRetirement() {
      if (this.income > 0) {
        return this.income - this.toSavings;
      }
      return 0;
    }
  },
  filters: {
    toUSD(value) {
      return value.toLocaleString(undefined, {
        currency: "USD",
        style: "currency"
      });
    }
  }
};
</script>

<style>
#app {
  margin-top: 30px;
}

#emoji {
  font-size: 500%;
}
</style>
